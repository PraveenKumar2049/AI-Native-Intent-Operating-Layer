import json
import re
from llm_client import ask_llm, ask_llm_stream, SYSTEM_PROMPT
from tool_router import execute_tool
from utils.logger import setup_logger
from memory.database import init_db, save_log


class Controller:

    def __init__(self):
        self.logger = setup_logger()
        init_db()

        self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

        self.MAX_HISTORY = 20
        self.last_sources = None
        self.pending_tool = None

        self.logger.info("Controller initialized")

    # =========================================================
    # MEMORY TRIM
    # =========================================================
    def trim_memory(self):
        if len(self.conversation) > self.MAX_HISTORY + 1:
            system = self.conversation[0]
            recent = self.conversation[-self.MAX_HISTORY :]
            self.conversation = [system] + recent

    # =========================================================
    # NON-STREAMING
    # =========================================================
    def process_input(self, user_input):

        try:
            lower = user_input.lower().strip()

            confirm = self._handle_confirmation(lower)
            if confirm:
                return confirm

            system_response = self._handle_system_commands(lower)
            if system_response:
                return system_response

            if "source" in lower or "link" in lower:
                return self.last_sources or "No sources available."

            self.conversation.append({"role": "user", "content": user_input})
            self.trim_memory()

            raw = ask_llm(self.conversation)

            if not raw or raw.strip() == "":
                return "Model returned empty response."

            parsed = self._safe_parse_json(raw)
            final = self._handle_parsed_response(parsed)

            self.conversation.append({"role": "assistant", "content": final})
            save_log(user_input, final)

            return final

        except Exception:
            self.logger.error("Controller error", exc_info=True)
            return "Something went wrong."

    # =========================================================
    # STREAMING
    # =========================================================
    def stream_input(self, user_input):

        try:
            lower = user_input.lower().strip()

            confirm = self._handle_confirmation(lower)
            if confirm:
                yield confirm
                return

            system_response = self._handle_system_commands(lower)
            if system_response:
                yield system_response
                return

            self.conversation.append({"role": "user", "content": user_input})
            self.trim_memory()

            stream = ask_llm_stream(self.conversation)

            buffer = ""

            for chunk in stream:
                token = self._extract_token(chunk)
                if token:
                    buffer += token

            if not buffer.strip():
                yield "Model returned empty response."
                return

            parsed = self._safe_parse_json(buffer)
            final = self._handle_parsed_response(parsed)

            yield final

            self.conversation.append({"role": "assistant", "content": final})
            save_log(user_input, final)

        except Exception:
            self.logger.error("Streaming error", exc_info=True)
            yield "Streaming error occurred."

    # =========================================================
    # CONFIRMATION HANDLER
    # =========================================================
    def _handle_confirmation(self, lower):

        if lower == "yes" and self.pending_tool:
            tool_name, args = self.pending_tool
            self.pending_tool = None
            return execute_tool(tool_name, args)

        if lower == "no" and self.pending_tool:
            self.pending_tool = None
            return "Action cancelled."

        return None

    # =========================================================
    # SYSTEM COMMANDS
    # =========================================================
    def _handle_system_commands(self, lower):

        if "shutdown" in lower:
            self.pending_tool = ("shutdown_pc", {})
            return "CONFIRM: Shutdown computer? YES/NO"

        if "restart" in lower:
            self.pending_tool = ("restart_pc", {})
            return "CONFIRM: Restart computer? YES/NO"

        if lower.startswith("delete file"):
            file_name = lower.replace("delete file", "").strip()
            if not file_name:
                return "Which file should I delete?"
            self.pending_tool = ("delete_file", {"file_name": file_name})
            return f"CONFIRM: Delete file '{file_name}'? YES/NO"

        return None

    # =========================================================
    # HANDLE PARSED RESPONSE (FIXED)
    # =========================================================
    def _handle_parsed_response(self, parsed):

        if not parsed:
            return "Model formatting error."

        # ✅ NORMAL RESPONSE
        if "response" in parsed:

            response_value = parsed["response"]

            # If already string → return directly
            if isinstance(response_value, str):
                return response_value

            # If model returned nested object → convert safely
            try:
                return json.dumps(response_value, indent=2)
            except Exception:
                return str(response_value)

        # ✅ TOOL CALL
        if "tool" in parsed:

            tool_name = parsed["tool"]
            args = parsed.get("arguments", {})

            if tool_name in ["delete_file", "shutdown_pc", "restart_pc"]:
                self.pending_tool = (tool_name, args)
                return f"CONFIRM: Run '{tool_name}'? YES/NO"

            if tool_name == "send_email":
                self.pending_tool = (tool_name, args)
                to = args.get("to", "")
                return f"CONFIRM: Send email to {to}? YES/NO"

            result = execute_tool(tool_name, args)

            if tool_name == "web_search":
                self.last_sources = result

            return result

        return str(parsed)

    # =========================================================
    # SAFE JSON PARSER (ROBUST + MODEL-TOLERANT)
    # =========================================================
    def _safe_parse_json(self, raw):

        if not raw or raw.strip() == "":
            return {"response": "Model returned empty response."}

        cleaned = raw.replace("```json", "").replace("```", "").strip()

        # 1️⃣ Try strict JSON
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # 2️⃣ Try extracting valid JSON object
        try:
            matches = re.findall(r"\{.*?\}", cleaned, re.DOTALL)
            for candidate in matches:
                try:
                    return json.loads(candidate)
                except Exception:
                    continue
        except Exception:
            pass

        # 3️⃣ Plain text fallback
        return {"response": cleaned}

    # =========================================================
    # TOKEN EXTRACTION
    # =========================================================
    def _extract_token(self, chunk):

        if not chunk:
            return ""

        if isinstance(chunk, dict):
            if "choices" in chunk:
                delta = chunk["choices"][0].get("delta", {})
                return delta.get("content", "")
            return chunk.get("content", "")

        return str(chunk)
