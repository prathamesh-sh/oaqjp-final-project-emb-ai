import json, sys, importlib.util, pathlib

proj = pathlib.Path('C:/Users/sprat/.gemini/antigravity/scratch/oaqjp-final-project-emb-ai/emotion_detection_raw.py')
sys.path.append(str(proj.parent))
spec = importlib.util.spec_from_file_location('emotion_detection_raw', str(proj))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
result = mod.emotion_detector('I love this new technology.')
print(result)
