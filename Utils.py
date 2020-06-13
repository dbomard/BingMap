def deg_decimal_to_sexa(val):
    deg = int(val)
    tmp_min = (val-float(deg))*60
    min = int(tmp_min)
    sec = tmp_min-float(min)
    sec = round(sec,2)
    return (deg, min, sec)

assert deg_decimal_to_sexa(48.858333) == (48,51,0.5)