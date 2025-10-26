#!/usr/bin/env python3
"""
Hostile Job Interview Audio Generator
Generates an AI audio file with interview questions and a heartbeat background
"""

import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine
import io
import os

def generate_heartbeat(duration_ms, bpm=80):
    """Generate a heartbeat sound (lub-dub pattern)"""
    # Calculate heartbeat interval
    beat_interval_ms = 60000 / bpm  # milliseconds per beat
    
    # Create lub-dub sounds
    # "Lub" - lower frequency, longer
    lub_freq = 40  # Hz
    lub_duration = 150  # ms
    
    # "Dub" - slightly higher frequency, shorter
    dub_freq = 60  # Hz
    dub_duration = 100  # ms
    
    # Pause between lub and dub
    lub_dub_gap = 100  # ms
    
    # Create the lub sound
    lub = Sine(lub_freq).to_audio_segment(duration=lub_duration)
    lub = lub.fade_in(20).fade_out(30)
    
    # Create the dub sound
    dub = Sine(dub_freq).to_audio_segment(duration=dub_duration)
    dub = dub.fade_in(15).fade_out(25)
    
    # Create silence
    gap = AudioSegment.silent(duration=lub_dub_gap)
    pause = AudioSegment.silent(duration=int(beat_interval_ms - lub_duration - dub_duration - lub_dub_gap))
    
    # Combine into one heartbeat cycle
    heartbeat_cycle = lub + gap + dub + pause
    
    # Repeat to fill duration
    num_cycles = int(duration_ms / len(heartbeat_cycle)) + 1
    heartbeat = heartbeat_cycle * num_cycles
    
    # Trim to exact duration
    heartbeat = heartbeat[:duration_ms]
    
    # Reduce volume
    heartbeat = heartbeat - 20  # Reduce by 20 dB
    
    return heartbeat

def text_to_speech(text, lang='en'):
    """Convert text to speech using gTTS"""
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save to bytes buffer
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Load as AudioSegment
    audio = AudioSegment.from_file(fp, format="mp3")
    return audio

def add_pause(duration_ms=1000):
    """Add a pause/silence"""
    return AudioSegment.silent(duration=duration_ms)

def generate_interview():
    """Generate the complete interview audio"""
    
    print("Generating interview segments...")
    
    # Interview script with hostile tone
    segments = []
    
    # Introduction
    intro = "Welcome to your interview. I hope you're prepared, because frankly, most candidates aren't. Now, organize yourselves into pairs or trios immediately. I don't have all day."
    segments.append(("Intro", text_to_speech(intro)))
    segments.append(("Pause", add_pause(2000)))
    
    # Question 1: Joke
    q1 = "First task. Each of you will tell a joke. And it better be funny. I've heard terrible jokes all day. Go ahead."
    segments.append(("Q1", text_to_speech(q1)))
    segments.append(("Pause", add_pause(15000)))  # 15 seconds for responses
    
    q1_eval = "Now discuss amongst yourselves. Who had the funniest joke? And be honest, most of you probably weren't funny at all. You have thirty seconds."
    segments.append(("Q1 Eval", text_to_speech(q1_eval)))
    segments.append(("Pause", add_pause(30000)))  # 30 seconds
    
    # Question 2: Challenge
    q2 = "Next question. Tell me about a time you faced a real challenge. Not some trivial inconvenience. A REAL challenge. Let's see if any of you have actually overcome anything meaningful."
    segments.append(("Q2", text_to_speech(q2)))
    segments.append(("Pause", add_pause(20000)))  # 20 seconds for responses
    
    q2_eval = "Alright. Discuss who faced the hardest challenge. Though I doubt any of these qualify as truly difficult. You have thirty seconds. Make it quick."
    segments.append(("Q2 Eval", text_to_speech(q2_eval)))
    segments.append(("Pause", add_pause(30000)))  # 30 seconds
    
    # Question 3: Secret
    q3 = "Final question. I want you each to share a secret. A personal secret. Something that actually means something to you. Don't waste my time with surface-level nonsense. Go."
    segments.append(("Q3", text_to_speech(q3)))
    segments.append(("Pause", add_pause(20000)))  # 20 seconds for responses
    
    q3_eval = "Now decide. Who shared the most personal secret? Who actually had the courage to be vulnerable? You have thirty seconds, then we're done here."
    segments.append(("Q3 Eval", text_to_speech(q3_eval)))
    segments.append(("Pause", add_pause(30000)))  # 30 seconds
    
    # Rejection
    rejection = "Well, that was... underwhelming. I'll be direct with you. None of you are what we're looking for. Your jokes were mediocre at best. Your challenges were mundane. And your secrets? Frankly, I've heard more interesting stories in a elevator. We won't be moving forward with any of you. This interview is over. Don't bother asking for feedback."
    segments.append(("Rejection", text_to_speech(rejection)))
    segments.append(("Pause", add_pause(2000)))
    
    # Combine all segments
    print("Combining interview segments...")
    interview_audio = AudioSegment.empty()
    for label, segment in segments:
        print(f"  Adding: {label}")
        interview_audio += segment
    
    # Generate heartbeat for the full duration
    print("Generating heartbeat...")
    total_duration = len(interview_audio)
    heartbeat = generate_heartbeat(total_duration, bpm=85)  # Slightly elevated heart rate for stress
    
    # Mix interview with heartbeat
    print("Mixing audio with heartbeat...")
    final_audio = interview_audio.overlay(heartbeat)
    
    return final_audio

def main():
    """Main function"""
    print("=" * 50)
    print("Hostile Job Interview Audio Generator")
    print("=" * 50)
    print()
    
    # Generate the interview
    audio = generate_interview()
    
    # Export to file
    output_file = "hostile_interview.mp3"
    print(f"\nExporting to {output_file}...")
    audio.export(output_file, format="mp3", bitrate="192k")
    
    print(f"\n✓ Audio file generated successfully!")
    print(f"  File: {output_file}")
    print(f"  Duration: {len(audio) / 1000:.1f} seconds")
    print()

if __name__ == "__main__":
    main()
