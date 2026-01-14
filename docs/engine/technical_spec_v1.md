# Technical Specification: Neural TTS & Voice Cloning

## 1. Model Selection: XTTS v2
The platform utilizes **XTTS v2** as its primary inference engine. This choice was made based on:
- **Zero-Shot Cloning:** Capability to clone a voice with only 6 seconds of reference audio.
- **Cross-Lingual Transfer:** The ability to take an English speaker's voice and make them speak fluent Thai while maintaining their unique vocal timbre and emotional nuances.
- **Latency:** Optimized for inference speeds under 2.0x RTF (Real-Time Factor) on NVIDIA T4/L4 GPUs.

## 2. Audio Processing Pipeline
1. **Denoising:** Input samples are passed through a DeepFilterNet to remove background noise before cloning.
2. **Feature Extraction:** GPT-style latent conditioning to capture the speaker's style.
3. **Vocoding:** Using a HiFi-GAN based vocoder integrated into the XTTS pipeline for high-frequency reconstruction (24kHz/44.1kHz).

## 3. Localization Logic
For the Thai market, we implement a custom **Grapheme-to-Phoneme (G2P)** layer to handle tonal complexities that standard multi-lingual models often struggle with. This ensures that the generated Thai speech is not just intelligible, but natural to native ears.