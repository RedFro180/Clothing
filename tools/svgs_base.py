"""Shared hoodie outline for sketch generators."""
INK="#1b1b1b"; FAB="#d8d0c0"
def hoodie(view):
    # simple flat boxy hoodie, 600x640 viewBox; view = front/back
    body = ('<path d="M150 170 L95 200 L40 470 L95 485 L130 330 L135 590 L465 590 L470 330 L505 485 L560 470 L505 200 L450 170 '
            'Q420 150 390 145 Q300 60 210 145 Q180 150 150 170 Z" fill="%s" stroke="#555" stroke-width="3"/>' % FAB)
    hood = ('<path d="M210 145 Q300 210 390 145" fill="none" stroke="#555" stroke-width="3"/>' if view=="front"
            else '<path d="M215 145 Q300 40 385 145 Q300 175 215 145 Z" fill="#cfc6b4" stroke="#555" stroke-width="3"/>')
    cuffs = ('<rect x="38" y="465" width="60" height="22" fill="#c9c0ad" stroke="#555" stroke-width="2" transform="rotate(5 68 476)"/>'
             '<rect x="502" y="465" width="60" height="22" fill="#c9c0ad" stroke="#555" stroke-width="2" transform="rotate(-5 532 476)"/>'
             '<rect x="135" y="560" width="330" height="30" fill="#c9c0ad" stroke="#555" stroke-width="2"/>')
    extra = ''
    if view=="front":
        extra = ('<path d="M200 430 L400 430 L420 520 L180 520 Z" fill="none" stroke="#777" stroke-width="2" stroke-dasharray="6 4"/>'
                 '<line x1="280" y1="190" x2="275" y2="250" stroke="#8a7f6a" stroke-width="3"/><line x1="320" y1="190" x2="325" y2="250" stroke="#8a7f6a" stroke-width="3"/>')
    return body+hood+cuffs+extra
