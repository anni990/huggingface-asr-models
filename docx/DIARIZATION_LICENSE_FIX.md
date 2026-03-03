# ⚠️ URGENT: Accept ALL Pyannote Model Licenses

## Your Current Error

```
Could not download 'pyannote/segmentation-3.0' model.
It might be because the model is private or gated...
```

## The Problem

The pyannote diarization pipeline uses **3 different gated models**, and you need to accept the license for **ALL of them**.

You've set your HuggingFace token ✅  
But you need to accept **3 model licenses** (not just 1!)

---

## ✅ THE FIX (Takes 1 minute)

### Accept Licenses for ALL 3 Models:

**Click each link below and accept the license:**

1. **Main Diarization Pipeline**
   ```
   https://huggingface.co/pyannote/speaker-diarization-3.1
   ```
   → Click "Agree and access repository"

2. **Segmentation Model** ← **THIS IS THE ONE FAILING NOW**
   ```
   https://huggingface.co/pyannote/segmentation-3.0
   ```
   → Click "Agree and access repository"

3. **Speaker Embedding Model**
   ```
   https://huggingface.co/pyannote/wespeaker-voxceleb-resnet34-LM
   ```
   → Click "Agree and access repository"

---

## How to Accept Each License

For **each model page** above:

1. Click the link
2. Scroll down the page
3. Find the **"Agree and access repository"** button
4. Click it
5. Move to the next model

You must do this for ALL 3 models!

---

## After Accepting All Licenses

**Restart your backend:**

```bash
# Stop the current server (Ctrl+C)
cd backend
python run.py
```

That's it! Diarization will work now.

---

## Verify It Works

After restarting, the diarization should load without errors:

```
✅ Loading diarization pipeline...
✅ Diarization pipeline loaded successfully
```

Instead of:

```
❌ Could not download 'pyannote/segmentation-3.0' model
❌ 'NoneType' object has no attribute 'eval'
```

---

## Quick Checklist

- [ ] Accept license: pyannote/speaker-diarization-3.1
- [ ] Accept license: pyannote/segmentation-3.0 ← **MOST IMPORTANT**
- [ ] Accept license: pyannote/wespeaker-voxceleb-resnet34-LM
- [ ] Restart backend server
- [ ] Test transcription with diarization

---

## Still Having Issues?

Make sure you're logged into HuggingFace with the same account that has the token!

1. Go to https://huggingface.co/
2. Make sure you're logged in
3. Accept all 3 licenses
4. Wait 1-2 minutes for permissions to propagate
5. Restart backend

**Your token is already set correctly in `.env`** ✅
