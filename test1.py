import cv2, math, numpy as np, arabic_reshaper
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from bidi.algorithm      import get_display
from PIL                 import ImageFont, ImageDraw, Image
from collections         import deque, Counter
import builtins, io
import sys



if hasattr(sys.stdout, "reconfigure"):
    # Python 3.7+ only: switch stdout to UTF‑8
    sys.stdout.reconfigure(encoding="utf-8")

_open_orig = builtins.open
def _open_utf8(path, mode='r', *args, **kwargs):
    # Only rewrite the labels2.txt reads
    if isinstance(path, str) and path.endswith("labels2.txt"):
        # drop any existing encoding kwarg so we only pass one
        kwargs.pop('encoding', None)
        return _open_orig(path, mode, encoding='utf-8', *args, **kwargs)
    # otherwise just fall back to the normal open
    return _open_orig(path, mode, *args, **kwargs)

builtins.open = _open_utf8

# ───────────────────────── config ─────────────────────────
MODEL_PATH   = "Models/keras_model_12.h5"
LABELS_PATH  = "Models/labels2.txt"
##FONT_PATH    = "C:/Users/aboo7/Downloads/newSignLan/font/NotoNaskhArabic-Regular.ttf"
FONT_PATH    = "static/font/NotoNaskhArabic-Regular.ttf"



IMG_SIZE     = 400
OFFSET       = 20
BASE_THRESH  = 0.80
WINDOW       = 7
CLASS_THRESH = {
    "ولادة": 0.60,
    "طبيب": 0.65, 
    "التهاب": 0.96 ,
    "موعد": 0.65 ,
    "رجال": 0.98 ,
    "شكرا": 0.65 ,
    "3": 0.60 ,
    "9": 0.60 ,
    "6": 0.99 ,
    "أ": 2.00 ,
    
    "ب": 2.00,
    "ت": 2.00,
    "ث": 2.00,
    "ج": 2.00,
    "ح": 2.00,
    "خ": 2.00,
    "د": 2.00,
    "ذ": 2.00,
    "ر": 2.00,
    "ز": 2.00,
    "س": 2.00,
    "ش": 2.00,
    "دق عليا": 2.00,

}          # optional per‑class overrides
# ──────────────────────────────────────────────────────────

cap        = cv2.VideoCapture(0)
detector   = HandDetector(maxHands=2)
classifier = Classifier(MODEL_PATH, LABELS_PATH)

votes      = deque(maxlen=WINDOW)

with open(LABELS_PATH, encoding="utf-8") as f:
    labels = [ln.strip().split(" ", 1)[1] for ln in f if " " in ln]

def draw_arabic(img, text, pos, font=FONT_PATH, size=32, color=(255,255,255)):
    reshaped = arabic_reshaper.reshape(text)
    bidi_txt = get_display(reshaped)
    pil      = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ImageDraw.Draw(pil).text(pos, bidi_txt,
                             font=ImageFont.truetype(font, size),
                             fill=color)
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

# ───────────────────────── main loop ─────────────────────
while True:
    ok, frame = cap.read()
    if not ok:
        break

    out = frame.copy()
    hands, frame = detector.findHands(frame)

    # ─── Hand‑pose filtering: keep only hands with full landmark set ───
    valid = [h for h in hands if h.get("lmList") and len(h["lmList"]) == 21]

    if valid:
        # union bbox of 1–2 valid hands
        xs, ys, ws, hs = zip(*[h['bbox'] for h in valid])
        x_min = max(min(xs) - OFFSET, 0)
        y_min = max(min(ys) - OFFSET, 0)
        x_max = min(max([x+w for x,w in zip(xs,ws)]) + OFFSET, frame.shape[1])
        y_max = min(max([y+h for y,h in zip(ys,hs)]) + OFFSET, frame.shape[0])

        try:
            crop = frame[y_min:y_max, x_min:x_max]
            if crop.size == 0:
                raise ValueError("empty crop")

            canvas = np.ones((IMG_SIZE, IMG_SIZE, 3), np.uint8) * 255
            h_c, w_c = crop.shape[:2]
            r = h_c / w_c
            if r > 1:
                k = IMG_SIZE / h_c
                w_ = math.ceil(k * w_c)
                canvas[:, (IMG_SIZE-w_)//2:(IMG_SIZE+w_)//2] = cv2.resize(crop, (w_, IMG_SIZE))
            else:
                k = IMG_SIZE / w_c
                h_ = math.ceil(k * h_c)
                canvas[(IMG_SIZE-h_)//2:(IMG_SIZE+h_)//2, :] = cv2.resize(crop, (IMG_SIZE, h_))

            preds, idx = classifier.getPrediction(canvas, draw=False)
            conf       = preds[idx]
            votes.append((idx, conf))

            idx_mode, freq = Counter(v[0] for v in votes).most_common(1)[0]
            conf_avg = np.mean([v[1] for v in votes if v[0] == idx_mode])
            need     = CLASS_THRESH.get(labels[idx_mode], BASE_THRESH)

            if freq >= WINDOW//2 and conf_avg >= need:
                # *** NEW LINE: print the raw Arabic label to the console ***
                print(labels[idx_mode], flush=True)

                txt = f"{labels[idx_mode]}  {conf_avg:.2f}"
                cv2.rectangle(out, (x_min, y_min-50), (x_min+320, y_min-10), (255,0,255), 3)
                out = draw_arabic(out, txt, (x_min+10, y_min-45))
                cv2.rectangle(out, (x_min, y_min), (x_max, y_max), (255,0,255), 3)

            cv2.imshow("Crop",  crop)
            cv2.imshow("White", canvas)

        except Exception as e:
            print("⚠️", e)

    cv2.imshow("Webcam", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
