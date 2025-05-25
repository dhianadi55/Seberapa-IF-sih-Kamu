# main.py

import cv2
import json
import time
import numpy as np
import pygame
import sys
from quiz_logic import Quiz
from head_tracker import HeadTracker

pygame.mixer.init()

def play_sound(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def draw_button(frame, text, center, size=(300, 60), color=(0, 140, 255)):
    x, y = center
    w, h = size
    top_left = (x - w // 2, y - h // 2)
    bottom_right = (x + w // 2, y + h // 2)
    cv2.rectangle(frame, top_left, bottom_right, color, -1, cv2.LINE_AA)

    max_width = 260
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
    display_text = text
    while text_size[0] > max_width and len(display_text) > 4:
        display_text = display_text[:-1]
        text_size = cv2.getTextSize(display_text + "...", cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
    if text_size[0] > max_width:
        display_text = display_text[:10] + "..."
    cv2.putText(
        frame,
        display_text + ("..." if text_size[0] > max_width else ""),
        (x - w // 2 + 10, y + 5),
        cv2.FONT_HERSHEY_DUPLEX,
        0.6,
        (0, 0, 0),
        1
    )

def highlight_frame(frame, color=(0, 255, 0), thickness=10):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, h), color, thickness)
    return frame

def ensure_landscape(frame):
    h, w = frame.shape[:2]
    if h > w:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return frame

def draw_informatics_frame(frame):
    color = (0, 255, 0)
    thickness = 2
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (10, 10), (w - 10, h - 10), color, thickness)
    corner_size = 25
    for x in [10, w - 10 - corner_size]:
        for y in [10, h - 10 - corner_size]:
            cv2.rectangle(frame, (x, y), (x + corner_size, y + corner_size), color, 1)

def show_final_score(quiz, questions):
    result_frame = np.zeros((480, 854, 3), dtype=np.uint8)
    cv2.putText(result_frame, "Skor Akhir Anda:", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.putText(result_frame, f"{quiz.score} / {len(questions)}", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    start_time = time.time()
    while time.time() - start_time < 5:
        cv2.imshow("Hasil Akhir", result_frame)
        if cv2.getWindowProperty("Hasil Akhir", cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def main():
    # Load questions
    with open("assets/soal.json", "r") as f:
        questions = json.load(f)
    quiz = Quiz(questions)
    tracker = HeadTracker()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    last_answer_time = 0
    waiting_for_neutral = False

    while quiz.has_next_question() and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = ensure_landscape(frame)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (854, 480))

        # Cooldown logic
        time_since_last_answer = time.time() - last_answer_time
        if time_since_last_answer < 3:
            cooldown_time = 3 - int(time_since_last_answer)
            cv2.putText(frame, f"Cooldown: {cooldown_time}s", (300, 240), font, 1.5, (0, 0, 255), 3)
            cv2.imshow("Seberapa IF Kamu?", frame)
            key = cv2.waitKey(1) & 0xFF
            if cv2.getWindowProperty("Seberapa IF Kamu?", cv2.WND_PROP_VISIBLE) < 1:
                break
            if key == ord('q'):
                break
            waiting_for_neutral = True  # Setelah cooldown, wajib netral dulu
            continue

        arah = tracker.detect_direction(frame)
        question = quiz.current_question()
        if question is None:
            break

        # Overlay for question background
        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (834, 80), (10, 50, 90), -1, cv2.LINE_AA)
        alpha = 0.7
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # Draw question and options
        cv2.putText(frame, question['question'], (40, 60), font, 0.8, (0, 255, 0), 2)
        draw_button(frame, f"A: {question['option_a']}", center=(240, 160), color=(0, 200, 255))
        draw_button(frame, f"B: {question['option_b']}", center=(620, 160), color=(0, 255, 100))
        draw_informatics_frame(frame)

        # Draw answer hints
        cv2.putText(frame, "← Jawab A", (40, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, "Jawab B →", (640, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)

        # Handle answer
        if waiting_for_neutral:
            if arah is None:
                waiting_for_neutral = False  # Kepala sudah netral, siap menerima input lagi
            # Jangan proses jawaban apapun sebelum netral
        elif arah:
            answer = "A" if arah == "left" else "B"
            quiz.answer_current_question(answer)
            highlight_color = (0, 255, 0) if answer == question["answer"] else (0, 0, 255)
            frame = highlight_frame(frame, highlight_color, 20)
            sound = "assets/sound_ping.mp3" if answer == question["answer"] else "assets/sound_beep.mp3"
            play_sound(sound)
            cv2.imshow("Seberapa IF Kamu?", frame)
            cv2.waitKey(500)
            if cv2.getWindowProperty("Seberapa IF Kamu?", cv2.WND_PROP_VISIBLE) < 1:
                break
            quiz.next_question()
            last_answer_time = time.time()
            waiting_for_neutral = True  # Setelah jawab, wajib netral dulu
            continue

        cv2.imshow("Seberapa IF Kamu?", frame)
        key = cv2.waitKey(1) & 0xFF
        if cv2.getWindowProperty("Seberapa IF Kamu?", cv2.WND_PROP_VISIBLE) < 1:
            break
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    show_final_score(quiz, questions)
    sys.exit()

if __name__ == "__main__":
    main()