"""
STT Configuration
Safe standalone config file.
Does NOT modify any existing AI_OS logic.
"""

MODEL_SIZE = "base"  # tiny | base | small
DEVICE = "cpu"  # cpu | cuda
COMPUTE_TYPE = "int8"  # int8 for lightweight CPU
SAMPLE_RATE = 16000
