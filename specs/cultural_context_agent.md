# Agent Specification: Culture-Sync Translation Engine
**Status:** Draft | **Version:** 1.1.0
**Role:** Translation & Cultural Context Agent (TCCA)

## 1. Objective
To bridge the gap between literal translation and cultural resonance. The Culture-Sync Agent ensures that content translated from any source language (e.g., Thai) feels native to the target audience (e.g., US, Spain, Brazil) by adapting idioms, humor, and social references while maintaining the original creator's intent and timing.

## 2. Core Capabilities
- **Idiomatic Transcreation:** Moving beyond word-for-word translation to find "functional equivalents" in the target culture.
- **Linguistic Timing Optimization:** Adjusting word choice to match the original audio's duration (syllable count management) for better lip-syncing.
- **Sentiment & Tone Preservation:** Detecting the emotional nuance (sarcastic, formal, enthusiastic) and ensuring the target text carries the same weight.
- **Glossary Management:** Maintaining consistency for brand names, technical terms, or creator-specific catchphrases.

## 3. Agent Logic Flow
1. **Context Extraction:** Analyze the video category (Gaming, Edu, Vlog) and creator persona.
2. **Initial NMT Pass:** Generate a base translation using a high-fidelity LLM (e.g., GPT-4o or Llama 3).
3. **Cultural Filtering:** Identify "At-Risk" phrases (slang, local metaphors, specific cultural events).
4. **Localization Refinement:** Replace "At-Risk" phrases with culturally relevant alternatives.
5. **Prosody Alignment:** Final polish to ensure the sentence length allows for natural TTS pacing.

## 4. Input/Output Schema
- **Input:** JSON (Source Text, Source Lang, Target Lang, Tone, Category, Time Constraints).
- **Output:** JSON (Translated Text, Cultural Notes, Phonetic Guide, Timing Confidence Score).