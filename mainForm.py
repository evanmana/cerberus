from pathlib import Path
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import sqlite3
from cryptography.fernet import Fernet
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
import csv


class Cerberus:
    @staticmethod
    def getAppIcon():
        appIcon = """
                iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAMAAABhq6zVAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAA
                AOpgAAA6mAAAF3CculE8AAABrVBMVEV4j6N4jqN1iqZ0iqWgwLCgwLD/2k//2k/szWDszWD////35pr35pray2ray2oAAADJoG3JoGz/
                9pzgoYffoYX/85p3jqN2jKB+lqp/l6t+lqt+lqt/l6t+lap2jKB3jqN5kKp1iqV/l7F/lrF/lrF/l7F1iqV5kKqeva+OsqKkxLOkxLOk
                xLOkxLOOsqKdva9ziZ96kaeCoK2OrrOOrrOCoK16kadziZ+FlJxigaqao5+YpaaYpKaao59jgqqEk5z3zU61sIWWp6uWp6u1sIX3zU7c
                wGF8l7NvjrJvjrJ8l7PcwWH////p1oXg2KL56qH56qHg2KLp1ob////045fo04bowInowIjo04b04pfawXPWx2TozovgxITgxITozovW
                x2TawXPPqHLFn2Haq4Laq4LFoGLPqXLfyXzit4bLl3TUn33Un33Ll3XitoXfyH1+lrB+lrCkxLOkxLOOrrSQrrOQr7OOrrSlraWUoqiT
                oqilraWTpq6YpqaYpqWTpq7PwYK8wKa9wabPwYLr4aTr4aT98KLWqHvWqHv98KLds4bds4bgtonhton////6RKx9AAAAcHRSTlMAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAA0DJvL6+vMk/AwVt+///+20FBIr5/f35igRqwOf+/ufBaxJM0P390U0TRvD+/vBGYvz///xhAbX8///8
                tQEEffr6fQQBGOL7++IYAQI29vU1AgADW8LBWQMAHcsDdwAAAAFiS0dECmjQ9FYAAAAHdElNRQfjCxAPChiZEpLjAAAApElEQVQI12MQ
                YxCXkJSSlpGVY5RnUGBSLFBSVlEtVGNWZ9Bg0SzS0tbRLdZj1WcwMDQqMS4tMyk3NTNnsLC0qrCurLKptrWzZ2BzcKxxqq1zrndxZWfg
                cGtw92hs8vRq9uZk8OHybfHzDwhsDeIKZgjhDm0La+8I74zgiWSI4o2O6YqN645P4Etk4E8SSE7p6U1NE0znZ8gQyhTOys7JFckTzQcA
                Zo8nNXAdmh0AAAAldEVYdGRhdGU6Y3JlYXRlADIwMTktMTEtMTZUMTU6MTA6MjQtMDg6MDBWiWGPAAAAJXRFWHRkYXRlOm1vZGlmeQAy
                MDE5LTExLTE2VDE1OjEwOjI0LTA4OjAwJ9TZMwAAAABJRU5ErkJggg==
                """
        return appIcon

    @staticmethod
    def getSearchIcon():
        searchIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMA
                    AA7DAcdvqGQAAAD4SURBVDhPtZK9TsMwFIUzsLAVxF51Dh1SBpZKDKAYFNshW9nasR1AQmKhZeBn6dL36QPxBjwAn6WjDHWJsASf
                    dBWdc32Pb6Jk/0pd1/1Qkr+nqqoL59wbw4+hrLUvPMdqd8OgoVYMHMsKgTd4a+pK1n442OO2D8mW4DN8Tu+1LMsj2THe+0sO3UlG
                    hF7nFjTJ8E4yggDLNreSMbz3KSEPkhGE39MfSu6HS545eCbZws0jekvJn9EHeydkFjZqmiZncIr31PkBd2HomuEFIfMQSE3USoet
                    BgR8GWNOZKXDRltqI5kOG4Qf6ZM6lJUOr5IXRXEg+Rdk2Tea80eK5t/XLAAAAABJRU5ErkJggg==
                    '''
        return searchIcon

    @staticmethod
    def getAddIcon():
        addIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAOElEQVQokWNgoBJwgGIMwEQtDTgB
                    yRoYcTgBxj6AJHaAgYHhAMk24AINUIwBaO9pZjxyD6CYMgAA6/MG0do6pCsAAAAASUVORK5CYII=
                    '''
        return addIcon

    @staticmethod
    def getEditIcon():
        editIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAXElEQVQokcXNoQ2AQBBE0ZeAowLq
                    oRE6AYlDUAF90AVFUMZhViHuDkGYZLLmz18+yIylFu5wIsVQWzD3GHDEKAun6BafquCE6R94fMBzDn7as+YmbosLO9aS/VVuPnQe
                    CUPPWjYAAAAASUVORK5CYII=
                    '''
        return editIcon

    @staticmethod
    def getDeleteIcon():
        deleteIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAoUlEQVQokb2OMQ6CUBBEZ792xuPA
                    7+GfhCBBg17GQoKJJ+ECxuPgTyyQsTCEFX+r0+3szO4D/ibvbOGTOP/ykzj3zhbjbNSup6Du0minjmQU1AOGxejJ7EtGsiF4MGIe
                    JBsK9+v2dgoWptJwhgAEKh2eI02Sdzqkj4JCqkTMRijHzkXbYNM7m93TuNeBkKc/LIUoNfOqvV6EKA3MMwz4C70A3ZVMHzoSQQYA
                    AAAASUVORK5CYII=
                    '''
        return deleteIcon

    @staticmethod
    def getInfoIcon():
        infoIcon = '''
                   iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAARElEQVQokWNgoAJQYWBguAPFKuiST
                   Fg0+DMwMChDsR+xNtxmYGC4BdVEffAfit+QowkDYPM0XkB7DYxYxNDdjk0N8QAA5qgK0QnW7YsAAAAASUVORK5CYII=
                    '''
        return infoIcon

    @staticmethod
    def getExcelIcon():
        excelIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAABK0lEQVQokZWRzUoCYRSGn+8bhcai
                    gSgHjLDctLAfaycULdsU0RXUtpuIghZdQRfQBURBqzYtIoIgs3TaBGqGxczYQmgGQfRrUQ1jBeG7fM95zjmcF3qU+Gmkd7JDWqc5
                    JzrCuNvLHf0JzG7PLysltkBlgCSAFtUeEjOJw6BRifPT9ePrCICCLKi18KSBWP+YqZv7ZiyO1/IoNcq7wCcAMD6cZDWzQr6aR4/q
                    3NsFzYzFmR6ewvYdSo0yAPIbqNSfSI2k2FzY4OLxkj5N1+JfQMqYCDbL0BVoUhKREaTosrsUnJQeTXNTyVF9e2ZpcpHcy23b8R0K
                    9SK27/wGrJqFVbOCgmEMtm3fgXoRr+V1AwKuFOIk/Nb3pvfqeu6B67kAKKnOghzC+i+4nvUBGuFnrHFS+BMAAAAASUVORK5CYII=
                     '''
        return excelIcon

    @staticmethod
    def getExitIcon():
        exitIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAArElEQVQokZXRsWpCQRCF4S96A1fQ
                    wpR5Fe0E7Wyt0ljapAxok8rKUmx9DQvtfIe8QkCwsggoIc1c0ORuLh447MDOP3OW5U49xPmEMeqJvgvWOBYNrxjigEaJB2hhnwWQ
                    Y4v3X5OfY8gsemT+1zSgD5xTQBedqD/xgj4WKSBHO+rH8HdxWQZsw7DEJiKBWsUb5hgV+a83fKGHtwTYwY7bj5ugmQBOWOFYkeiv
                    fgCGpRoLVq8K4wAAAABJRU5ErkJggg==
                     '''
        return exitIcon

    @staticmethod
    def getSettingsIcon():
        settingsIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAdUlEQVQoka3RTQqCABQE4I8O0An0
                    HIG30OyKeYJ05cVEqM0rXoKl4MBshpn3ywGoMAerX8YaF4x4BsfQ6qX5lkxrbOEUgSaFHyhQYkj6NXc4Y4pKRdLL0KbwfDrsRpdm
                    7RcjvfV7DrT+L/21AzvPmrH5cZvwAiTzLK0qoOjqAAAAAElFTkSuQmCC
                     '''
        return settingsIcon

    @staticmethod
    def getLogoIcon():
        logoIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAABmJLR0QA/wD/AP+gvaeTAAAN80lEQVR4nO2ceXQd1X3Hv/femTdv
                    kZ42bCPJkkCKTGwoNkvDoZCCiBdwISa0GGh6avB6cnqgpSfLcZo0anKaNqE9tCbdIE0pqZM4FKhjcLzgFBxI44INuNjGsbVZsnZL
                    72nem/3e2z+EhWW9Z400I1lq/flLnnnznTtf37nL7/7uAJe4xMWEhCHyaOOWpG3zdBha04XHneT3vv0lPaiOEkphPFHOGNMrrrii
                    MAy9qeZ0a6vOoJQDCGwgDaE84IJXMEXhYWhNB4rCOJO0IgytUAwESDlTFBaO1tTDFJVJoDwMrVAMlJJUMFWJhqE1HSiKqkkqZ04N
                    pIRWM6aoYWhNB0xhESqV6jC0QjKQ1M6iNxiUMYDJ2lC0whCRBPMZC6VDnxYURYEE5oehFU4nIuU8psweA6nCQCTmhaIVhogUsoSy
                    2fMKK0yBFLI0DK3ABj7auCUpAUppSCOiaYBQCgnQtV/8VuCBf+CnHp6FUCuoznRDGbUYUwKPBQMbONtmIWcJazYSQstPyh3bLm5v
                    agouNb0UkxBmI4ENdOemHyqbUySX37I4lMjOdLHnzfdkf2/qIQA/DKITvOUnsjKhabPKPABIaBqhjFQG1QluIMW8glgssMx0k4jF
                    IakIPBYMwUCRTMRnn4EF8SgEkUVBdQIbKCiPJQtnn4GFBTGAicARpOA1UBEsWTBrIlkjFBVGAcYDd6Ijjf/GzU/KoGL/n3j6Lx4n
                    wHnDmPm1tSBk1nWo04qUEh3NzSP/HnmFCSEv9nd3ZYUQF6VgswEhBM50d2cJYf9x9tiIgQOR1EOO5WzrPtWhm9nsxSnhDMY0DHSf
                    6tAt03whouPBs8fHvK+bNv/1SlDlO4qqlCWLS5KxRByEzJ5IS5hIKWFmDeipwSHXdbPw+Of+6Vt/vP3c3+Rp8CTZ9CdP3g2wP4OU
                    ixLJAsQThVokqv2fN1NKCce2YOpZJ5PRBUBaIbxvD2hDW59vbHTO//24PcbGzX/1cQL6EAhbLaWoUzUtE4snktFYjKlaBLMpDpgL
                    IQRc14VtGtLKGrpj2zFC0C6l3EZAf/CP3/zD9y90/YS63Ec2b5kTkXwpKPlNQsltgssFqiJYPB4DYREQRYOqqlBUFZSxGdSjS3Au
                    4DkuXNcB91zAs2FZJhyXcMpIMwRe51LsVz13798/8cVuv8qBnvD+xsbIA3OO2DXXr0DXGY6OXoG+FEcqw2FYAgqjUFUKpjBQqgBU
                    gSQMjFEQUBBKQSgBAQFlo2syoQQUBBLDtQQApJCQcni4KiWHlARSCkBKyA9NIsIDpAchBATncFwOzxOIaRTFBQouK6KonENQOUdB
                    26Hd2H/8k9GnnnrMnqwHgavInmfulMt++7NjjntcIp0VGMpKZEyBjCGQsQT0LGDaEqYLmLaA7Ug4LmC7H5okh4vkcgnOh81ijEBl
                    w8cJGT6mqRQRhUDTgGiEIB4BYhpFYQIoiFIUxCkKYhTJOEVRAYHCxj7q3he2YvmGXYE8mLKlNIURlCUZypJTdYeZwezuAWYAE66+
                    u/9h+VymsodB2T0E8sptJ5YGDkpeTB6of/U0KGkWrrfDZeTZlWt/2jeR6ydk4N7v3rWWELKlaE4pKyopjka0CL75UhWq6uomVuoZ
                    QntTE778mXY4lo30YNpK9w9wSPEHS9fv+le/Gr5f4V3/vKKBKmxL/bULE1W1NdFkSRGi8RiKNBOWMfumfqZhIKmZiMZjSJYWo6qu
                    Jlp/7aIEVZS/2/P0Xbf51fFtoEqVb1ReUZXQYqNjf/XJJjjZ8LN7jUwWfR2t6Gxphj7YByDcaJubTWFBcvRKohbTUF5TlWAq+4Zf
                    Hd8GSoFrC4vHdqlVBV2wbRvc9fxKjYvwPGQGe/HofYX4y8+VoFgzkRkKnI07Anc92LaNqoKuMecKS5IQQiz2q+XfQClilI7Nf2FE
                    4DeuicLIhFcLM3oaNy3S8LH5CpJxilW3xuBZQ6HpG9k0brkmCkbGhu4YZYCUcb9avg2klOie5+Y813CdBjOjj8wSgiCEgKkP4c5P
                    fLTOclVVBJ7jgnvBa7mUEqau4/brtJznPdcFIcT3/5ZvAwmhx82MkfPc3BKG6rkMYcQRzWwGtRUqyoo+KhpjwOL6CMxsJrC+kcmg
                    ep6CuSW5s8mMrAFC6Qd+9XwbKFzxk6FUOm8S0bIbNTjZlF+5vHimjoYcteOmhRFwK7iBrpHGshsiec/rg2mTc7497w/Ow38NpPhB
                    qn9Ayjwh/1+r0wDpwbEnPS8H9zzYtoNrasemW3+8WoXrecjXjPjBtW1AesNlzYEQAqkzg5CU+0738G3gp9bvbAPIm/3dfTkzsSgF
                    bl8ShR1gSGNmM1hcH8k58aeU4No6NVAzYWXTuH1JFPlCmGe6+zxQ8tqKtXva/WpOaC4sOR7r6ei0vDyNecN1UZhGFvnOXwjOOUw9
                    haXX519jXnZDFKaempS+57qwjCwarsut77kuejq6bJd7j09Ed0IGLtvwyjEp5N+0HW/Sc/W3iRjB6tviSPWchpHJwM8Kn+ACRkbH
                    YFcHVt4cRc3l+QNEVfMU3H9bHIPdHcjqOgT3oS8EzGwW6d5OrL4jgURsbO2WAFqPN+kS8sm71u06Pq7oOUw4nPVmx01/emv1Wze1
                    HWu6ueaq2sT5529dHEVZMcNLPx9EV0cfHPfCD6lFKKrnKVhzbxxXVedv3M/yycUaKucwbH8jhZbOftjOhfUjKkXFZQp+79MJLKwZ
                    27ZKIdF6vClrGdYv3jz1ia8BO8ctw7lMKpj44x/fHynNZJ9TFGWlYzuFuQKqs4G9L2yFqkUy0vN+knR7Hr5x08EJ91CTCqiuXv28
                    A+DB3c8sX0ZA90xGY6bALfszSzfufnWy1wcKqK7YsGdvkOtnAkHMAy5FpANzycCABDaQgHiCz7pdDhCcg1Ay+WnNhwRelaMKS9uW
                    WRZLFEzoOttw0HqkHd1N3TCGTDi2C/9BU4KIpiKejKG87nLUXF0FLT7+EGjU/U0TjCqBJ++BDWSUvjc0eOYO/wZKnDjYghNvN6E4
                    WYzLEnMQLY1ieLus31GVhOdxmLaJ/pMDOHmoGfW/Xof666/0rZEe7Adh7F2fN8xL8H0irvdyX0/nzfPm14ybKC0lcHDXe0j3DKH+
                    igWIqJPdo02gKAoKlUIUJgoxt3QO2g6fwlDvEG64czH8mNjf3Wm4jvPKJAswQuA2UBJ3W+/pU76mVR/88lcY6tVRV1UbwLyxqGoE
                    dVW1GOrW8cGBk+P+XgiO3tPtVGXYFvTegQ1cvm5vJwV9u7uj5YINWDZloPVwG2oqaqYkRY4QiuqKGrS824psOnfg9yxdp5olpeSX
                    DY/s9J1ElI9QUjscz/tK09HDr5RX1xbky8hqeb8NJcVlUM7Z2e44Djp7TyNjZOC5E+vJFZUhkShA5dxKRNThDkRRFJQWlaLt/TYs
                    umVhzuuklGg6+r7h2e5XJ3TDfOUIQ2TF+p37f/bsPUdPt568cf6V9TmrV09zHyrLRm+OPNXVBpsMQL3MRIRMcD1FEhgZA+1dHuqq
                    60cOJwuL0NncmdfAjuYTQnB+eNmmXW9M7Ia5CS25SLjuhl8dfue/5lVWx9XI2IivmTWhVYyOxVm2hRXrPg1FHbs+sf2p0VGRVY+u
                    HPMbz+XY/d19o45FNQ1mxsxZRte2cfLIe7bj2BvGfSCfhNYYLd2w6zAk+d7RQwdyNkDc42OyWT2X5zTvLEuuXoIlVy/Je15R2Zjg
                    KqUM3MvdHBw5eMCUUjx958bdR/KKTpBQW3NKhr4w0NN9pru9dcZt2ulqb5GDfd29ts6/FKZuqAY2PPKaxR3+W0cPHbD01GCY0oHI
                    pFM49s5/Gy6371752E8nv+qVg9DHE8s27fwfzsWmd37xn4Zj526LphPHtnDojZ+Z3BUbVqzfc8GE8ckwJdGY5et3ft9znCffen2P
                    4bmB5+uTxvM8HNy/1+Dce2L5hp2BdqbnY8rCWZ9a+8pXHMvedvDn+wzPdUApDSX1YzykFKCUwnMdHNz/qmGZ5rY7Ht7xtam635TG
                    AxvW7FiX1dNb33ptbzaiqXDPq42RSAT7nnsdxw6cgD7gP+tAH8jg2IET2Pfc64hERkdhHNeFFovgrdf2mIah/1vDmh3rQnmYPEzp
                    95oIgQRe3rjvX+4ZEIR+wbRMeu4DL6pfCMMwkWpJoe3wKSgaQ+VVlZhfP/ZjGvpABh0nutB5vBOu7aGosAgVpZWIn7db3rBMcNjC
                    toy/vWPNjs34/al8wpC+oeqHl5/4nW1F2rzVVRX5vjonh83MpJDW07Ate2QM+O6Rd6FFNRQVFqG4oPhD03IXva2jBbp35tm7P//8
                    I1PzJKOZti+G8azyeMpKr6osFxrNGUwgiMfjiMfjqJhbDsP4qAdfcOWCC5p2Fo97GNJ1y2Wxz4db+vxM25rIqsYfdQJkb19/n4+8
                    jGEzzzL89/gvS29/rytBXrrvy8+dCVDUCTGti0qCu5t6+ntNw7xwuGkyZIwszgz0GR4nfxS6+AWYVgNXNf6oUxC5obmt2bCd8CYE
                    pmWi5VSLIbh88L7G7/eGJuyDi7Kdcvuff3YtEfhO5eUV0dLiMjLZXZ1SSvQP9Iuunm5LELnm3q9u/feQizouF20/6otff2CxwtRn
                    GMiikuLSSGG8QI1Go2CKgtydDCCkAPc8mJYFPau7A6lBl0C+LT2+6Z7GH/pOyw2Ti76h98WvP7CYgf6uwlgDF/JjQsgEIHOuURJC
                    HEpIhlB6wnP5PoBsvbdx69HpLvMlLjFz+F+nsMc22sYlgQAAAABJRU5ErkJggg==
                     '''
        return logoIcon

    @staticmethod
    def getEnterIcon():
        enterIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAAuUlEQVQ4ja3TMW4CMRCF4S+BLnU6
                    kCi5AlXOQJGtkTgBVwg9FadImZITINEhFFKm4ABoBQUVabwrF453o80vjWSPx09vxjIdeYjWUxToZeoveMN3lYiLd7ihzAi8YICP
                    1OEdrzm7eA9R89hwoZE2Ak8YtRFLtTDGPpGv6WcEZ1gHB4uEyBarzjOI+fcW4AsTPId99YRFWwG4hkjSeQbxXyhxwClTP8EG8yoR
                    /4VPDBtcHbHE+a9Of+UHPSodYxC2OlgAAAAASUVORK5CYII=
                     '''
        return enterIcon

    @staticmethod
    def getEmailIcon():
        emailIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAAuUlEQVQ4ja3TMW4CMRCF4S+BLnU6
                    kCi5AlXOQJGtkTgBVwg9FadImZITINEhFFKm4ABoBQUVabwrF453o80vjWSPx09vxjIdeYjWUxToZeoveMN3lYiLd7ihzAi8YICP
                    1OEdrzm7eA9R89hwoZE2Ak8YtRFLtTDGPpGv6WcEZ1gHB4uEyBarzjOI+fcW4AsTPId99YRFWwG4hkjSeQbxXyhxwClTP8EG8yoR
                    /4VPDBtcHbHE+a9Of+UHPSodYxC2OlgAAAAASUVORK5CYII=
                     '''
        return emailIcon

    @staticmethod
    def getPasswordIcon():
        passwordIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAABSUlEQVQokW3SP0vXURQG8E/f0LCC
                    H2EgouJS4Jhbg2CYSOHg7BDoIr2AhoaGQIR6BwYNooMW4phOhQ0SCupoRDgIFpHRIJlk6XAfxcSznHv+Pefe57n8b9fwBB+wgwN8
                    wxsMod45dg8/cIjPeIlnmMBW8qtoPz3Uhz/YwzAunAGtw9MMf8TVi6jhPRowgDk8xChuoxkjmMQl9OIXPA7SeNDHEm8H/XfiLtzM
                    eR2WEnSiLY1f0JgNX1PvCPBP7FZJ7AflTpqnw+p+QOB7/F9UFa5gN6htKW7GV2jFP4XxmiLZpyrItWzaycCN+Pu4nsE6DIbx18Li
                    oaJjiyLJAeYV/VZSX0ptFZehP4Vl5Wfcxbs09uAW3mINz3O7E3uV4YVsPWsVmk4njn9IA17ggcLkIjbytmZFwxk8OgcUdGNKYXVP
                    YXsTs4pUJ3YETbpZWdfB700AAAAASUVORK5CYII=
                     '''
        return passwordIcon

    @staticmethod
    def getCopyIcon():
        copyIcon = '''
                     iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAA2UlEQVQokYXRMUvCURQF8F9/jIY
                     kCREay6lJV6VJam1qMOgzONTYl2htzKHJrxC1NRUOLg6B0WCiFK0FkcN7wr9H0oEzvPvO5dxzL5xggvfIKc4twQpe0cRzrLVwhN
                     X4nuACH5ChkBNvo4tH3ESu4w6Vhcss53iIq2SKPfxggHIh+czwndSecIlNXKcNf6GKHm4x+69hCzU00CcEXoY2DjDCl9yWYCMRN
                     7Er3KWCjhBcJux4iAfUY0NRWPELTqPDL5RjuH3cYw2lRLOD8SLDW+QIx8L1U3zibA4B6SwnqfCn4AAAAABJRU5ErkJggg==
                      '''
        return copyIcon

    def __init__(self, master, root):
        self.versionApp, self.key = self.initApp()
        print(self.key)

        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus')
        self.windowWidth = 1060
        self.windowHeight = 450
        self.screenWidth = self.master.winfo_screenwidth()
        self.screenHeight = self.master.winfo_screenheight()
        self.positionRight = int(self.screenWidth / 2 - self.windowWidth / 2)
        self.positionDown = int(self.screenHeight / 3 - self.windowHeight / 2)
        self.master.geometry(
            "{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, self.positionRight, self.positionDown))

        self.img = PhotoImage(data=self.getAppIcon())
        self.master.wm_iconphoto(True, self.img)

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        self.addIcon = PhotoImage(data=self.getAddIcon())
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", image=self.addIcon, compound='left',
                             command=self.getAddNewServiceForm)
        self.editIcon = PhotoImage(data=self.getEditIcon())
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left',
                             command=self.getEditServiceForm)
        self.deleteIcon = PhotoImage(data=self.getDeleteIcon())
        filemenu.add_command(label="Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left',
                             command=self.deleteService)
        filemenu.add_separator()
        self.excelIcon = PhotoImage(data=self.getExcelIcon())
        filemenu.add_command(label="Εισαγωγή από Excel", image=self.excelIcon, compound='left', command=self.exportToCSV)
        filemenu.add_command(label="Εξαγωγή σε Excel", image=self.excelIcon, compound='left', command=self.exportToCSV)
        filemenu.add_separator()
        self.exitIcon = PhotoImage(data=self.getExitIcon())
        filemenu.add_command(label="Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)
        self.settingsIcon = PhotoImage(data=self.getSettingsIcon())
        settingsMenu.add_command(label="Επεξεργασία Στοιχείων", image=self.settingsIcon, compound='left',  command=self.getSettingsForm)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Βοήθεια", menu=aboutMenu)
        self.infoIcon = PhotoImage(data=self.getInfoIcon())
        aboutMenu.add_command(label="Περί", image=self.infoIcon, compound='left', command=self.getAboutAppForm)

        self.master.config(menu=self.menubar)

        self.copyIcon = PhotoImage(data=self.getCopyIcon())
        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label=" Αντιγραφή Email", image=self.copyIcon, compound='left',
                               command=self.copyEmail)
        self.popup.add_command(label=" Αντιγραφή Username", image=self.copyIcon, compound='left',
                               command=self.copyUsername)
        self.popup.add_command(label=" Αντιγραφή Κωδικού", image=self.copyIcon, compound='left',
                               command=self.copyPasswd)
        self.popup.add_command(label=" Αντιγραφή ID", image=self.copyIcon, compound='left',
                               command=self.copyID)
        self.popup.add_separator()
        self.popup.add_command(label=" Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left',
                               command=self.getEditServiceForm)
        self.popup.add_command(label=" Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left',
                               command=self.deleteService)
        self.popup.add_separator()
        self.popup.add_command(label=" Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        self.frame = Frame(self.master, background="white", borderwidth=1, relief="sunken",
                           highlightthickness=1)
        self.frame.pack(side="top", fill="x", padx=4, pady=4)

        self.search = StringVar()

        self.searchEntry = Entry(self.frame, textvariable=self.search, borderwidth=0, highlightthickness=0,
                                 background="white")
        self.searchEntry.insert(0, 'Αναζήτηση Υπηρεσίας')
        self.searchEntry['fg'] = 'grey'
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.searchService())

        self.searchEntry.image = PhotoImage(data=self.getSearchIcon())
        imageLabel = Label(self.frame, image=self.searchEntry.image)
        imageLabel.pack(side="left")
        imageLabel['bg'] = 'white'

        self.searchEntry.pack(side="left", fill="both", expand=True)

        # Fix BUG with Treeview colors in Python3.7
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style(root)
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        # Fix BUG with Treeview colors in Python3.7

        self.table = Treeview(self.master)
        self.table['show'] = 'headings'
        self.table['columns'] = ('Services', 'email', 'username', 'passwd', 'id', 'category', 'url')

        for col in self.table['columns']:
            self.table.heading(col, command=lambda c=col: self.sortby(self.table, c, 0))

        self.table.heading('Services', text='Services')
        self.table.column('Services', anchor='center', width=200)

        self.table.heading('email', text='Email')
        self.table.column('email', anchor='center', width=200)

        self.table.heading('username', text='Username')
        self.table.column('username', anchor='center', width=100)

        self.table.heading('passwd', text='Password')
        self.table.column('passwd', anchor='center', width=100)

        self.table.heading('url', text='URL')
        self.table.column('url', anchor='center', width=120)

        self.table.heading('id', text='ID')
        self.table.column('id', anchor='center', width=100)

        self.table.heading('category', text='Category')
        self.table.column('category', anchor='center', width=100)

        self.table.tag_configure('oddrow', background='#e6eef2')
        self.table.tag_configure('evenrow', background='#b3cfdd')
        self.table.tag_configure('focus', background='#c6b6b4')
        self.last_focus = None
        self.last_focus_tag = None
        self.table.focus()
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<<TreeviewSelect>>", self.onTableSelect)
        self.table.bind("<ButtonRelease-1>", self.openURLService)
        self.table.bind("<Motion>", self.changePointerOnHover)
        self.table.bind("<Button-3>", self.popupMenu)
        self.searchEntry.bind("<FocusIn>", self.foc_in)
        self.searchEntry.bind("<FocusOut>", self.foc_out)
        self.popup.bind("<FocusOut>",self.popupFocusOut)
        self.master.protocol("WM_DELETE_WINDOW", self.exitApp)

        self.loadTable(self)

        self.master.bind("<Escape>", self.exitApp)

    def popupFocusOut(self, event=None):
        self.popup.unpost()

    def foc_in(self, *args):
        if self.search.get() == 'Αναζήτηση Υπηρεσίας':
            self.searchEntry.delete('0', 'end')
            self.searchEntry['fg'] = 'black'

    def foc_out(self, *args):
        if not self.search.get():
            self.searchEntry.insert(0, 'Αναζήτηση Υπηρεσίας')
            self.searchEntry['fg'] = 'grey'
            self.loadTable(self)

    def changePointerOnHover(self, event):
        _iid = self.table.identify_row(event.y)

        if _iid != self.last_focus:
            if self.last_focus:
                self.table.item(self.last_focus, tags=[self.last_focus_tag])

            self.last_focus_tag = self.table.item(_iid, "tag")
            self.table.item(_iid, tags=['focus'])
            self.last_focus = _iid

        curItem = self.table.item(self.table.identify('item', event.x, event.y))
        if curItem['values'] != '':
            col = self.table.identify_column(event.x)
            url = curItem['values'][int(col[-1]) - 1]

            if col[-1] == "7" and url != '---':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")

    def openURLService(self, event):
        curItem = self.table.item(self.table.focus())
        col = self.table.identify_column(event.x)
        region = self.table.identify("region", event.x, event.y)

        if col[-1] == "7" and region != 'heading':
            url = curItem['values'][int(col[-1]) - 1]
            if url != '---':
                webbrowser.open_new_tab('http://' + str(url))

    def onTableSelect(self, event):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            print(item_text[0])

    def getSelectedService(self, event):
        for item in self.table.selection():
            selectedRow = self.table.item(item, "value")
            return selectedRow

    def initApp(self):
        print("Initialize Cerberus App")
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT version, masterToken FROM cerberusParameters")
        row = cur.fetchone()
        cur.close()

        return row

    def copyEmail(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[1])

    def copyUsername(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[2])

    def copyPasswd(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[3])

    def copyID(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[4])

    @staticmethod
    def getMasterToken():
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT  masterToken FROM cerberusParameters")
        masterToken = cur.fetchone()
        cur.close()

        return masterToken[0]

    def searchService(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()

        if self.search.get() == 'Αναζήτηση Υπηρεσίας':
            pass
        elif self.search.get():
            cur.execute(
                "SELECT name, email, username, password, value, category, url FROM service WHERE name LIKE '%" + self.search.get() + "%' or name LIKE '%" + self.search.get().upper() + "%'")  # ('%'+self.search.get()+'%',),'Α')
        elif not self.search.get():
            cur.execute(
                "SELECT name, email, username, password, value, category, url FROM service ")

        rows = cur.fetchall()
        cur.close()

        for k in self.table.get_children():
            self.table.delete(k)

        i = 1
        for row in rows:
            if (i % 2) == 0:
                tag = "oddrow"
            else:
                tag = "evenrow"

            self.table.insert('', 'end',
                              values=(row[0],
                                      self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5],
                                      row[6]), tags=tag)
            i = i + 1

    @staticmethod
    def exitApp(event=None):
        root.destroy()

    @staticmethod
    def getAboutAppForm():
        import aboutApp
        aboutApp.aboutApp()

    def getAddNewServiceForm(self):
        self.master.withdraw()
        import addNewServiceForm
        addNewServiceForm.addNewServiceForm(self)

    def getEditServiceForm(self):
        service = self.getSelectedService(self)

        if service is None:
            messagebox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ επιλέξτε την Υπηρεσία που θέλετε να Επεξεργαστείτε.")
        else:
            self.master.withdraw()
            import editServiceForm
            editServiceForm.editServiceForm(self, service)

    def getSettingsForm(self):
        import settingsForm
        settingsForm.settingsForm()

    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
                     command=lambda x=col: self.sortby(tree, col, int(not descending)))

    @staticmethod
    def loadTable(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT name, email, username, password, value, category, url value FROM service")

        rows = cur.fetchall()

        for row in self.table.get_children():
            self.table.delete(row)

        i = 1
        for row in rows:
            if (i % 2) == 0:
                tag = "oddrow"
            else:
                tag = "evenrow"

            self.table.insert('', 'end',
                              values=(row[0], self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5],
                                      row[6]), tags=tag)
            i = i + 1

        conn.close()

        self.last_focus = None
        self.table.selection()

    def deleteService(self):
        service = self.getSelectedService(self)

        if service is None:
            messagebox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ επιλέξτε την Υπηρεσία που θέλετε να Διαγράξετε.")
        else:
            msgBox = messagebox.askquestion('Διαγραφή: {}'.format(service[0]),
                                            'Είστε σίγουρος ότι θέλετε να διαγράψετε την Υπηρεσία: ''{}'' ?'.format(
                                                service[0]),
                                            icon='warning')
            if msgBox == 'yes':
                try:
                    conn = sqlite3.connect('cerberus.db')
                except sqlite3.Error as e:
                    print(e)
                sql = 'DELETE FROM service WHERE name=?'
                cur = conn.cursor()
                cur.execute(sql, (service[0],))
                conn.commit()
                conn.close()
                self.loadTable(self)

    def popupMenu(self, event):
        serviceId = self.table.identify_row(event.y)
        if serviceId:
            self.table.selection_set(serviceId)
            try:
                self.popup.tk_popup(event.x_root, event.y_root)
            finally:
                self.popup.grab_release()

    def exportToCSV(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT masterToken FROM cerberusParameters")
        masterToken = cur.fetchone()

        # TODO
        passwd = 'YUaMl3PfzNvyJLzlbPzVCb78wcobfLjhcXgACw9rvkk='

        if masterToken[0] == passwd:
            cur = conn.cursor()
            cur.execute("SELECT category, name, email, username, password, value, url value FROM service")

            rows = cur.fetchall()

            csvData = [['Κατηγορία', 'Υπηρεσία', 'Email', 'Όνομα Χρήστη', 'Κωδικός', 'ID', 'URL', ]]

            for row in rows:
                csvData = csvData + [[row[0],
                                      row[1],
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[5]).decode("utf-8"),
                                      row[6]
                                      ]]

            try:
                homeFolder = str(Path.home())
                filePath = filedialog.asksaveasfile(initialdir=homeFolder,
                                                    initialfile='cerberus.csv',
                                                    title="Επιλογή Αρχείου",
                                                    filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
                if filePath:
                    try:
                        with open(filePath.name, 'w') as csvFile:
                            csvFile = csv.writer(csvFile, delimiter='\t')
                            csvFile.writerows(csvData)
                        messagebox.showinfo("Μήνυμα Επιτυχίας",
                                            "Το αρχείο αποθηκέυτηκε με Επιτυχία στην τοποθεσία {}.".format(
                                                filePath.name))
                    except Exception as e:
                        messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")
            except Exception as e:
                print(e)
                messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")


if __name__ == "__main__":
    import platform

    print(platform.system())


    def check_password(failures=[1]):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT masterToken FROM cerberusParameters")
        row = cur.fetchone()
        cur.close()

        if entry.get() == row[0]:
            failures.clear()
            print('Logged in')
            root.withdraw()
            master = Toplevel()
            App = Cerberus(master, root)

        failures.append(1)
        if sum(failures) > 3:
            root.destroy()
            raise SystemExit('Unauthorized login attempt')
        else:
            entry.delete(0, 'end')
            root.title('Λάθος Κωδικός, παρακαλώ δοκιμάστε ξανά. Προσπάθεια %i/%i' % (sum(failures), 3))


    def exitApp():
        root.destroy()


    def sendPasswdToEmail():
        import sendEmail
        sendEmail.sendEmail()


    root = Tk()
    windowWidth = 720
    windowHeight = 300
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    positionDown = int(screenHeight / 3 - windowHeight / 2)
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

    img = PhotoImage(data=Cerberus.getAppIcon())
    root.wm_iconphoto(True, img)
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.9)
    root.title('Εισαγωγή Κωδικού')

    welcomeFrame = Frame(root, height=130, bg='#1e1e2f')
    welcomeFrame.pack(side="top", fill=BOTH)

    appIcon = PhotoImage(data=Cerberus.getLogoIcon())
    panel = Label(root, image=appIcon, bg='#1e1e2f').place(x=20, y=20)
    Label(welcomeFrame, text="Καλώς ορίσατε στον", font=("Comic Sans MS", 32), fg='white', bg='#1e1e2f').place(x=110,
                                                                                                               y=25)
    Label(welcomeFrame, text="Cerberus", font=("Helvetica", 32), fg='#d9ddff', bg='#1e1e2f').place(x=380, y=72)

    parent = Frame(root, bg='lightgrey')
    parent.pack(side="top", fill=BOTH, expand=True)

    Label(parent, text="Παρακαλώ εισάγεται τον Κωδικό σας:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
    entry = Entry(parent, show="*", width=40)
    entry.pack(side=TOP, pady=(0, 15))

    enterIcon = PhotoImage(data=Cerberus.getEnterIcon())
    b = Button(parent, borderwidth=1, text="Είσοδος", image=enterIcon, compound=LEFT, pady=8, width=120, command=check_password)
    b.pack(pady="7")

    forgotPasswdLbl = Label(parent, text='Ξεχάσατε τον Κωδικό σας?', font=(None, 8), fg='blue', bg='lightgrey')
    forgotPasswdLbl.pack()

    forgotPasswdLbl.bind("<Button-1>", lambda x: sendPasswdToEmail())
    forgotPasswdLbl.bind("<Motion>", forgotPasswdLbl.config(cursor="hand2"))
    entry.bind('<Return>', lambda x: check_password())
    root.bind("<Escape>", lambda x: exitApp())
    entry.focus_set()
    root.resizable(0, 0)
    root.mainloop()
#YUaMl3PfzNvyJLzlbPzVCb78wcobfLjhcXgACw9rvkk=