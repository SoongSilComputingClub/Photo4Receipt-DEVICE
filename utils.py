import cv2

# ▓▓ ▒▒ ░░
PER_75 = '▓'
PER_50 = '▒'
PER_25 = '░'
PER_0 = '   '


def getImage(path: str, resize_rate: float) -> object:
    img = cv2.imread(path)
    img = cv2.resize(img, (0, 0), fx=resize_rate, fy=resize_rate, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hei, wid = img.shape[:2]
    return gray, hei, wid


def getAA_01(value: int) -> str:
    """gray value값을 기반으로 (▓▓, ▒▒, ░░,  ) 해당 밀도 블록으로 return함"""
    if value >= 255 * 75 / 100:
        return PER_0
    elif value >= 255 * 50 / 100:
        return PER_25
    elif value >= 255 * 25 / 100:
        return PER_50
    return PER_75
