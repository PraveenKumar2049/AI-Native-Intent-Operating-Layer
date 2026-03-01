#!/usr/bin/env python3
"""
AI_OS - Main Entry Point

This is a modular AI-powered operating layer prototype.
It demonstrates how a local LLM can interpret natural language
and execute structured system actions safely.

Author: AI_OS Team
Purpose: College Competition Demo
"""

import sys
from controller import Controller
from utils.logger import setup_logger
open 
def main():
    """
    Entry point for AI_OS application.
    
    Initializes the controller and starts the main interaction loop.
    No business logic here - just initialization and delegation.
    """
    # Setup logging
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("AI_OS Starting...")
    logger.info("=" * 60)
    
    # Print welcome message
    print("\n" + "=" * 60)
    print("🤖 AI_OS - Intelligent Operating System Layer")
    print("=" * 60)
    print("\nWelcome! I'm your AI assistant.")
    print("I can help you with:")
    print("  • Opening applications")
    print("  • Managing files")
    print("  • Setting reminders")
    print("  • Searching the web")
    print("  • Managing emails")
    print("\nType 'exit' or 'quit' to stop.")
    print("=" * 60 + "\n")
    
    try:
        # Initialize controller
        controller = Controller()
        
        # Start main loop
        controller.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down AI_OS...")
        logger.info("AI_OS stopped by user (Ctrl+C)")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        logger.info("AI_OS shutdown complete")
        print("Goodbye!\n")

if __name__ == "__main__":
    main()
