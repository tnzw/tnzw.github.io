# re_compilesearch.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def re_compilesearch():

  _registry = {
    "spaces": {
      " ":["\u00a0"],  # XXX please more spaces !
    },
    "ponctuation": {
      "...":["…"],
    },
    "default": {  # chars that look like latin letters
      "A":["Á","Ă","Ắ","Ặ","Ằ","Ẳ","Ẵ","Ǎ","Â","Ấ","Ậ","Ầ","Ẩ","Ẫ","Ä","Ǟ","Ȧ","Ǡ","Ạ","Ȁ","À","Ả","Ȃ","Ā","Ą",        "Å","Ǻ","Ḁ","Ⱥ","Ã","Ɐ","ᴀ"],
      "a":["á","ă","ắ","ặ","ằ","ẳ","ẵ","ǎ","â","ấ","ậ","ầ","ẩ","ẫ","ä","ǟ","ȧ","ǡ","ạ","ȁ","à","ả","ȃ","ā","ą","ᶏ","ẚ","å","ǻ","ḁ","ⱥ","ã","ɐ","ₐ"],
      "AA":["Ꜳ"],"AE":["Æ","Ǽ","Ǣ","ᴁ"],"AO":["Ꜵ"],"AU":["Ꜷ"],"AV":["Ꜹ","Ꜻ"],"AY":["Ꜽ"],
      "aa":["ꜳ" ],"ae":["æ","ǽ","ǣ","ᴂ"],"ao":["ꜵ" ],"au":["ꜷ"],"av":["ꜹ" ,"ꜻ"],"ay":["ꜽ"],
      "B":["Ḃ","Ḅ","Ɓ","Ḇ","Ƀ","Ƃ","ʙ","ᴃ"],
      "b":["ḃ","ḅ","ɓ","ḇ","ᵬ","ᶀ","ƀ","ƃ"],  # should we add the german ß ?
      "C":["Ć","Č","Ç","Ḉ","Ĉ",    "Ċ","Ƈ","Ȼ","Ↄ","Ꜿ","ᴄ"],
      "c":["ć","č","ç","ḉ","ĉ","ɕ","ċ","ƈ","ȼ","ↄ","ꜿ",   ],
      "D":["Ď","Ḑ","Ḓ",    "Ḋ","Ḍ","Ɗ",    "Ḏ","Đ","Ƌ",        "Ɖ","Ꝺ","ᴅ"],
      "d":["ď","ḑ","ḓ","ȡ","ḋ","ḍ","ɗ","ᶑ","ḏ","đ","ƌ","ᶁ","ᵭ","ɖ","ꝺ"    ],
      "DZ":["Ǳ","Ǆ"],
      "dz":["ǳ","ǆ"],
      "E":["É","Ĕ","Ě","Ȩ","Ḝ","Ê","Ế","Ệ","Ề","Ể","Ễ","Ḙ","Ë","Ė","Ẹ","Ȅ","È","Ẻ","Ȇ","Ē","Ḗ","Ḕ","Ę",        "Ɇ","Ẽ","Ḛ","Ɛ",    "Ǝ","ᴇ","ⱻ"],
      "e":["é","ĕ","ě","ȩ","ḝ","ê","ế","ệ","ề","ể","ễ","ḙ","ë","ė","ẹ","ȅ","è","ẻ","ȇ","ē","ḗ","ḕ","ⱸ","ę","ᶒ","ɇ","ẽ","ḛ","ɛ","ᶓ","ɘ","ǝ","ₑ"],
      "ET":["Ꝫ"],
      "et":["ꝫ"],
      "F":["Ḟ","Ƒ","Ꝼ","ꜰ"],
      "f":["ḟ","ƒ","ᵮ","ᶂ","ꝼ"],
      "ff":["ﬀ"],"ffi":["ﬃ"],"ffl":["ﬄ"],"fi":["ﬁ"],"fl":["ﬂ"],
      "G":["Ǵ","Ğ","Ǧ","Ģ","Ĝ","Ġ","Ɠ","Ḡ",    "Ǥ","Ᵹ","Ɡ","ɢ","ʛ"],
      "g":["ǵ","ğ","ǧ","ģ","ĝ","ġ","ɠ","ḡ","ᶃ","ǥ","ᵹ","ɡ",    "ᵷ"],
      "H":["Ḫ","Ȟ","Ḩ","Ĥ","Ⱨ","Ḧ","Ḣ","Ḥ","Ħ","ʜ"],
      "h":["ḫ","ȟ","ḩ","ĥ","ⱨ","ḧ","ḣ","ḥ","ɦ","ẖ","ħ","ɥ","ʮ","ʯ"],
      "hv":["ƕ"],
      "I":["Í","Ĭ","Ǐ","Î","Ï","Ḯ","İ","Ị","Ȉ","Ì","Ỉ","Ȋ","Ī","Į","Ɨ","Ĩ","Ḭ","ɪ"],
      "i":["ı","í","ĭ","ǐ","î","ï","ḯ","ị","ȉ","ì","ỉ","ȋ","ī","į","ᶖ","ɨ","ĩ","ḭ","ᴉ","ᵢ"],
      "IJ":["Ĳ"],"IS":["Ꝭ"],
      "ij":["ĳ"],"is":["ꝭ"],
      "J":["Ĵ","Ɉ","ᴊ"],
      "j":["ȷ","ɟ","ʄ","ǰ","ĵ","ʝ","ɉ","ⱼ"],
      "K":["Ḱ","Ǩ","Ķ","Ⱪ","Ꝃ","Ḳ","Ƙ","Ḵ","Ꝁ","Ꝅ","ᴋ"],
      "k":["ḱ","ǩ","ķ","ⱪ","ꝃ","ḳ","ƙ","ḵ","ᶄ","ꝁ","ꝅ","ʞ"],
      "L":["Ĺ","Ƚ","Ľ","Ļ","Ḽ","Ḷ","Ḹ","Ⱡ","Ꝉ","Ḻ","Ŀ","Ɫ","ǈ","Ł","Ꞁ","ʟ","ᴌ"],
      "l":["ĺ","ƚ","ɬ","ľ","ļ","ḽ","ȴ","ḷ","ḹ","ⱡ","ꝉ","ḻ","ŀ","ɫ","ᶅ","ɭ","ł","ꞁ"],
      "LJ":["Ǉ"],
      "lj":["ǉ"],
      "M":["Ḿ","Ṁ","Ṃ","Ɱ","Ɯ","ᴍ"],
      "m":["ḿ","ṁ","ṃ","ɱ","ᵯ","ᶆ","ɯ","ɰ"],
      "N":["Ń","Ň","Ņ","Ṋ","Ṅ","Ṇ","Ǹ","Ɲ","Ṉ","Ƞ","ǋ","Ñ","ɴ","ᴎ"],
      "n":["ń","ň","ņ","ṋ","ȵ","ṅ","ṇ","ǹ","ɲ","ṉ","ƞ","ᵰ","ᶇ","ɳ","ñ"],
      "NJ":["Ǌ"],
      "nj":["ǌ"],
      "O":[    "Ó","Ŏ","Ǒ","Ô","Ố","Ộ","Ồ","Ổ","Ỗ","Ö","Ȫ","Ȯ","Ȱ","Ọ","Ő","Ȍ","Ò","Ỏ","Ơ","Ớ","Ợ","Ờ","Ở","Ỡ","Ȏ","Ꝋ","Ꝍ",   "Ō","Ṓ","Ṑ","Ɵ","Ǫ","Ǭ","Ø","Ǿ","Õ","Ṍ","Ṏ","Ȭ","Ɔ","ᴏ","ᴐ"],
      "o":["ɵ","ó","ŏ","ǒ","ô","ố","ộ","ồ","ổ","ỗ","ö","ȫ","ȯ","ȱ","ọ","ő","ȍ","ò","ỏ","ơ","ớ","ợ","ờ","ở","ỡ","ȏ","ꝋ","ꝍ","ⱺ","ō","ṓ","ṑ",    "ǫ","ǭ","ø","ǿ","õ","ṍ","ṏ","ȭ","ɔ","ᶗ","ᴑ","ᴓ","ₒ"],
      "OE":["Œ","ɶ"],"OI":["Ƣ"],"OO":["Ꝏ"],"OU":["Ȣ","ᴕ"],
      "oe":["ᴔ","œ"],"oi":["ƣ"],"oo":["ꝏ"],"ou":["ȣ"],
      "P":["Ṕ","Ṗ","Ꝓ","Ƥ","Ꝕ","Ᵽ","Ꝑ","ᴘ"],
      "p":["ṕ","ṗ","ꝓ","ƥ","ᵱ","ᶈ","ꝕ","ᵽ","ꝑ"],
      "Q":["Ꝙ","Ꝗ"],
      "q":["ꝙ","ʠ","ɋ","ꝗ"],
      "R":["Ꞃ","Ŕ","Ř","Ŗ","Ṙ","Ṛ","Ṝ","Ȑ","Ȓ","Ṟ","Ɍ","Ɽ","ʁ","ʀ","ᴙ","ᴚ"],
      "r":["ꞃ","ŕ","ř","ŗ","ṙ","ṛ","ṝ","ȑ","ɾ","ᵳ","ȓ","ṟ","ɼ","ᵲ","ᶉ","ɍ","ɽ","ɿ","ɹ","ɻ","ɺ","ⱹ","ᵣ"],
      "S":["Ꞅ","Ś","Ṥ","Š","Ṧ","Ş","Ŝ","Ș","Ṡ","Ṣ","Ṩ","ꜱ"],
      "s":["ꞅ","ſ","ẜ","ẛ","ẝ","ś","ṥ","š","ṧ","ş","ŝ","ș","ṡ","ṣ","ṩ","ʂ","ᵴ","ᶊ","ȿ"],
      #"SS":["ß"],  # ß is normaly concidered lower cased
      "ss":["ß"],"st":["ﬆ"],
      "T":["Ꞇ","Ť","Ţ","Ṱ","Ț","Ⱦ","Ṫ","Ṭ","Ƭ","Ṯ","Ʈ","Ŧ","ᴛ"],
      "t":["ꞇ","ť","ţ","ṱ","ț","ȶ","ẗ","ⱦ","ṫ","ṭ","ƭ","ṯ","ᵵ","ƫ","ʈ","ŧ","ʇ"],
      "TZ":["Ꜩ"],
      "tz":["ꜩ"],
      "th":["ᵺ"],
      "U":["Ú","Ŭ","Ǔ","Û","Ṷ","Ü","Ǘ","Ǚ","Ǜ","Ǖ","Ṳ","Ụ","Ű","Ȕ","Ù","Ủ","Ư","Ứ","Ự","Ừ","Ử","Ữ","Ȗ","Ū","Ṻ","Ų","Ů","Ũ","Ṹ","Ṵ","ᴜ"],
      "u":["ᴝ","ú","ŭ","ǔ","û","ṷ","ü","ǘ","ǚ","ǜ","ǖ","ṳ","ụ","ű","ȕ","ù","ủ","ư","ứ","ự","ừ","ử","ữ","ȗ","ū","ṻ","ų","ᶙ","ů","ũ","ṹ","ṵ","ᵤ"],
      "ue":["ᵫ"],"um":["ꝸ"],
      "V":["Ʌ","Ꝟ","Ṿ","Ʋ","Ṽ","ᴠ"],
      "v":["ʌ","ⱴ","ꝟ","ṿ","ʋ","ᶌ","ⱱ","ṽ","ᵥ"],
      "VY":["Ꝡ"],
      "vy":["ꝡ"],
      "W":["Ẃ","Ŵ","Ẅ","Ẇ","Ẉ","Ẁ","Ⱳ","ᴡ"],
      "w":["ʍ","ẃ","ŵ","ẅ","ẇ","ẉ","ẁ","ⱳ","ẘ"],
      "X":["Ẍ","Ẋ"],
      "x":["ẍ","ẋ","ᶍ","ₓ"],
      "Y":["Ý","Ŷ","Ÿ","Ẏ","Ỵ","Ỳ","Ƴ","Ỷ","Ỿ","Ȳ","Ɏ","Ỹ","ʏ"],
      "y":["ʎ","ý","ŷ","ÿ","ẏ","ỵ","ỳ","ƴ","ỷ","ỿ","ȳ","ẙ","ɏ","ỹ"],
      "Z":["Ź","Ž","Ẑ","Ⱬ","Ż","Ẓ","Ȥ","Ẕ","Ƶ","ᴢ"],
      "z":["ź","ž","ẑ","ʑ","ⱬ","ż","ẓ","ȥ","ẕ","ᵶ","ᶎ","ʐ","ƶ","ɀ"],
    },
    "greek": {  # symbols that look/sound like ascii ones
      "A":["Α","Δ","Λ"],"a":["α"],
      "B":["Β"],"b":["β"],
      "C":["Ͼ","χ"],"c":["ͼ","χ"],
      "D":["Δ"],"d":["δ"],
      "E":["Ε","Η","Ξ","Σ"],"e":["ε","η","ξ"],
      "PH":["Φ"],"ph":["φ"],
      "G":["Γ"],"g":["γ"],
      "H":["Η"],"h":["λ"],
      "I":["Ι"],"i":["ι"],
      "K":["Κ"],"k":["κ"],
      "L":["Λ"],"l":["λ"],
      "M":["Μ"],"m":["μ"],
      "N":["Ν"],"n":["η","ν"],
      "O":["Θ","Ο","Φ","Ω"],"o":["θ","ο","σ","ω"],
      "P":["Π","Ρ","ψ"],"p":["π","ρ","ψ"],
      "Q":["Φ"],"q":["φ"],
      "R":["Π","Ρ"],"r":["π","ρ"],
      "S":["Σ"],"s":["ς","σ"],
      "T":["Θ","Τ"],"t":["θ","τ"],
      "U":["Υ"],"u":["μ","υ"],
      "v":["ν"],
      "w":["ω"],
      "X":["Ξ","Χ"],"x":["ξ","χ"],
      "Y":["Υ","Ψ"],"y":["γ","ψ"],
      "Z":["Ζ"],"z":["ζ"],
    },
    "katakana": {
      # https://fr.wikipedia.org/wiki/Katakana
      # romaji: katakana
      "a":["ア"],"i":["イ"],"u":["ウ"],"e":["エ"],"o":["オ"],
      "ka":["カ"],"ki":["キ"],"ku":["ク"],"ke":["ケ"],"ko":["コ"],
      "sa":["サ"],"shi":["シ"],"su":["ス"],"se":["セ"],"so":["ソ"],
      "ta":["タ"],"chi":["チ"],"tsu":["ツ"],"te":["テ"],"to":["ト"],
      "na":["ナ"],"ni":["ニ"],"nu":["ヌ"],"ne":["ネ"],"no":["ノ"],
      "ha":["ハ"],"hi":["ヒ"],"fu":["フ"],"he":["ヘ"],"ho":["ホ"],
      "ma":["マ"],"mi":["ミ"],"mu":["ム"],"me":["メ"],"mo":["モ"],
      "ya":["ヤ"],"yu":["ユ"],"yo":["ヨ"],
      "ra":["ラ"],"ri":["リ"],"ru":["ル"],"re":["レ"],"ro":["ロ"],
      "wa":["ワ"],"wi":["ヰ"],"we":["ヱ"],"wo":["ヲ"],            "o":["ヲ"],  # accept o as wo
      "n":["ン"],
      "ga":["ガ"],"gi":["ギ"],"gu":["グ"],"ge":["ゲ"],"go":["ゴ"],
      "za":["ザ"],"ji":["ジ"],"zu":["ズ"],"ze":["ゼ"],"zo":["ゾ"],
      "da":["ダ"],"ji":["ヂ"],"zu":["ヅ"],"de":["デ"],"do":["ド"],
      "ba":["バ"],"bi":["ビ"],"bu":["ブ"],"be":["ベ"],"bo":["ボ"],
      "pa":["パ"],"pi":["ピ"],"pu":["プ"],"pe":["ペ"],"po":["ポ"],
      "kya":["キャ"],"kyu":["キュ"],"kyo":["キョ"],
      "gya":["ギャ"],"gyu":["ギュ"],"gyo":["ギョ"],
      "sha":["シャ"],"shu":["シュ"],"sho":["ショ"],
      "ja":["ジャ"],"ju":["ジュ"],"jo":["ジョ"],
      "cha":["チャ"],"chu":["チュ"],"cho":["チョ"],
      "nya":["ニャ"],"nyu":["ニュ"],"nyo":["ニョ"],
      "hya":["ヒャ"],"hyu":["ヒュ"],"hyo":["ヒョ"],
      "bya":["ビャ"],"byu":["ビュ"],"byo":["ビョ"],
      "pya":["ピャ"],"pyu":["ピュ"],"pyo":["ピョ"],
      "mya":["ミャ"],"myu":["ミュ"],"myo":["ミョ"],
      "rya":["リャ"],"ryu":["リュ"],"ryo":["リョ"],
    },
    "hiragana": {
      # https://fr.wikipedia.org/wiki/Hiragana
      # romaji: hiragana
      "a":["あ"],"i":["い"],"u":["う"],"e":["え"],"o":["お"],
      "ka":["か"],"ki":["き"],"ku":["く"],"ke":["け"],"ko":["こ"],
      "sa":["さ"],"shi":["し"],"su":["す"],"se":["せ"],"so":["そ"],
      "ta":["た"],"chi":["ち"],"tsu":["つ"],"te":["て"],"to":["と"],
      "na":["な"],"ni":["に"],"nu":["ぬ"],"ne":["ね"],"no":["の"],
      "ha":["は"],"hi":["ひ"],"fu":["ふ"],"he":["へ"],"ho":["ほ"],
      "ma":["ま"],"mi":["み"],"mu":["む"],"me":["め"],"mo":["も"],
      "ya":["や"],"yu":["ゆ"],"yo":["よ"],
      "ra":["ら"],"ri":["り"],"ru":["る"],"re":["れ"],"ro":["ろ"],
      "wa":["わ"],"wi":["ゐ"],"we":["ゑ"],"wo":["を"],            "o":["を"],  # accept o as wo
      "n":["ん"],
      "ga":["が"],"gi":["ぎ"],"gu":["ぐ"],"ge":["げ"],"go":["ご"],
      "za":["ざ"],"ji":["じ"],"zu":["ず"],"ze":["ぜ"],"zo":["ぞ"],
      "da":["だ"],"ji":["ぢ"],"zu":["づ"],"de":["で"],"do":["ど"],
      "ba":["ば"],"bi":["び"],"bu":["ぶ"],"be":["べ"],"bo":["ぼ"],
      "pa":["ぱ"],"pi":["ぴ"],"pu":["ぷ"],"pe":["ぺ"],"po":["ぽ"],
      "kya":["きゃ"],"kyu":["きゅ"],"kyo":["きょ"],
      "gya":["ぎゃ"],"gyu":["ぎゅ"],"gyo":["ぎょ"],
      "sha":["しゃ"],"shu":["しゅ"],"sho":["しょ"],
      "ja":["じゃ"],"ju":["じゅ"],"jo":["じょ"],
      "cha":["ちゃ"],"chu":["ちゅ"],"cho":["ちょ"],
      "nya":["にゃ"],"nyu":["にゅ"],"nyo":["にょ"],
      "hya":["ひゃ"],"hyu":["ひゅ"],"hyo":["ひょ"],
      "bya":["びゃ"],"byu":["びゅ"],"byo":["びょ"],
      "pya":["ぴゃ"],"pyu":["ぴゅ"],"pyo":["ぴょ"],
      "mya":["みゃ"],"myu":["みゅ"],"myo":["みょ"],
      "rya":["りゃ"],"ryu":["りゅ"],"ryo":["りょ"],
    },
  }

  #def reverse_keys_and_values(d, o=None):
  #  # {"a":["b"],"c":["b","f"],"d":["e"]} -> {"b":["a","c"],"e":["d"],"f":["c"]}
  #  if o is None: o = {}
  #  for k, vv in d.items():
  #    for v in vv:
  #      if v in o: o[v].append(k)
  #      else: o[v] = [k]
  #  return o

  def merge_keys_and_values(d, *dd, lower_keys=False):
    # like d |= d2 | d3 | …
    if lower_keys:
      for d2 in dd:
        for k, vv in d2.items():
          k = k.lower()
          if k in d: d[k].extend(vv)
          else: d[k] = list(vv)
    else:
      for d2 in dd:
        for k, vv in d2.items():
          if k in d: d[k].extend(v for v in vv if v not in d[k])
          else: d[k] = list(vv)
    return d

  def _join(iterable, sep, begin, end):
    """\
_join(['a'], '|', '(?:', ')') -> \"a\"
_join(['a', 'b'], '|', '(?:', ')') -> \"(?:a|b)\"
"""
    border = [False]
    it = iter(iterable)
    def __iter__():
      for _ in it:
        yield _
        break
      for _ in it:
        border[0] = True
        yield _
        break
      for _ in it: yield _
    joined = sep.join(__iter__())
    if border[0]: return begin + joined + end
    return joined

  def mk_translater(d, bidirectional=True):  # XXX ignore_case=False
    # d => {a:["ä", "à"],ae:["æ"],…}
    # return => {a:"[aäà]","ä":"[aäà]","à":"[aäà]",ae:"(?:ae|æ)","æ":"(?:ae|æ)",…}
    # with ignore case return => {a:"[aAäÄàÀ]",…}  # XXX NIY
    res = {}
    for k in d:
      keys = [k]; chars = []; strings = []
      if k[1:2]: strings.append(k)
      elif k: chars.append(k)

      for v in d[k]:
        if bidirectional: keys.append(v)
        if v[1:2]: strings.append(v)
        elif v: chars.append(v)

      reg = _join(chars, "", "[", "]")
      reg = _join(([reg] if reg else []) + strings, "|", "(?:", ")")

      for i, k in enumerate(keys):
        if k:
          if i == 0 or k not in d or len(d[k]) == 0:
            res[k] = reg
    return res

  #assert(_=> js(mkTranslater({a:["ä","à"],ae:["æ"]})) === '{"a":"[aäà]","ae":"(?:æ|ae)"}');
  #assert(_=> js(mkTranslater({a:["ä","à"],ae:["æ"]}, true)) === '{"a":"[aäà]","ä":"[aäà]","à":"[aäà]","ae":"(?:æ|ae)","æ":"(?:æ|ae)"}');

  def str_compilesearch(search_string, translater):
    # search_string => "hello"
    # translater => {"a":"[aäà]","ae":"(?:ae|æ)","æ":"(?:ae|æ)",…}

    # searchforintramatch : {"x":"[xẍẋᶍ]","th":"ᵺ","hv":"ƕ","vf":"…","ffi":"…","fi":"…"}  (maxLen here is 3 → ffi, maxNo = maxLen - 2 = 1, possibleNo = 0)
    #   "abthvfficde"
    #   search a : set [[a]]
    #   search ab : "ab" no, so add [a] to regex and set [[b]]
    #   search abt : "abt" no, "bt" no, so add [b] to regex and set [[t]]
    #   search bth : "bth" no, "th" YES, add h [[t,h]]
    #                          getpossiblebegin []
    #                               set for th [[t,h], [th]]
    #                             possibleNo = maxNo
    #   search thv : "thv" no, "hv" YES, add v [[t,h,v],[th,v]]
    #                          getpossiblebegin [[t]]
    #                               set for hv [[t,h,v],[th,v], [t,hv]]
    #                             possibleNo = maxNo
    #   search hvf : "hvf" no, "vf" YES, add f [[t,h,v,f],[th,v,f],[t,hv,f]]
    #                          getpossiblebegin [[t,h],[th]] (len 2)
    #                               set for vf [[t,h,v,f],[th,v,f],[t,hv,f], [t,h,vf],[th,vf]] (+2 additions)
    #                             possibleNo = maxNo
    #   search vff : "vff" no, "ff" no, possibleNo-- (retain f [f])
    #   search ffi : "ffi" YES, "fi" YES, add retained [[t,h,v,f,f],[th,v,f,f],[t,hv,f,f],[t,h,vf,f],[th,vf,f]]
    #                                            add i [[t,h,v,f,f,i],[th,v,f,f,i],[t,hv,f,f,i],[t,h,vf,f,i],[th,vf,f,i]]
    #                                 getpossiblebegin [[t,h,v],[th,v],[t,hv]] (len 3)
    #                                      set for ffi [[t,h,v,f,f,i],[th,v,f,f,i],[t,hv,f,f,i],[t,h,vf,f,i],[th,vf,f,i], [t,h,v,ffi],[th,v,ffi],[t,hv,ffi]] (+3 additions)
    #                                 getpossiblebegin [[t,h,v,f],[th,v,f],[t,hv,f],[t,h,vf],[th,vf]] (len 5)
    #                                       set for fi [[t,h,v,f,f,i],[th,v,f,f,i],[t,hv,f,f,i],[t,h,vf,f,i],[th,vf,f,i], [t,h,v,ffi],[th,v,ffi],[t,hv,ffi], [t,h,v,f,fi],[th,v,f,fi],[t,hv,f,fi],[t,h,vf,fi],[th,vf,fi]] (+5 additions)
    #                               possibleNo = maxNo
    #   search fic : "fic" no, "ic" no, possibleNo-- (retain c [c])
    #   search icd : "icd" no, "cd" no, possibleNo is 0 → add [big truc] to regex ! add retained [c] to regex ! set [[d]]
    #   search cde : "cde" no, "de" no, possibleNo is 0 → add [d] to regex ! set [[e]]
    #   end : add [e] to regex

    translater_max_length = max(len(k) for it in (translater, ("1",)) for k in it)
    reg = ""
    _set, setl = [], 0
    retained = []
    max_no = max(0, translater_max_length - 2)
    possible_no = 0
    for i, c in enumerate(search_string):
      last_chars = search_string[max(0, i - translater_max_length + 1):i + 1]
      found = []
      while last_chars[1:2]:
        if translater.get(last_chars):
          found.append(last_chars)
        last_chars = last_chars[1:]
      if found:
        # lastChars found in translater

        # add retained to all set entries
        for r in retained:
          for s in _set: s.append(r)
        setl += len(retained)
        retained[:] = ()

        # add last char to all set entries
        for s in _set: s.append(last_chars)
        setl += 1

        # add all found in set
        for f in found:
          # add found in set when possible
          if setl - len(f) <= 0:
            _set.append([f])
          else:
            additions = []
            for s in _set:
              p = 0
              for j, v in enumerate(s):
                p += len(v)
                if p == setl - len(f):
                  additions.append(s[:j + 1] + [f])
                  #break
            for a in additions: _set.append(a)

        possible_no = max_no
      elif possible_no:
        possible_no -= 1
        retained.append(last_chars)
      else:
        # lastChars not found in translater

        # add set to re
        for j, group in enumerate(_set): _set[j] = "".join(translater.get(c) or re_escape(c) for c in group)
        if len(_set) == 0: pass
        elif len(_set) == 1: reg += _set[0]
        else: reg += "(?:" + "|".join(_set) + ")"
        _set[:], setl = (), 0

        # add retained to re
        for r in retained: reg += translater.get(r) or re_escape(r)
        retained[:] = ()

        # add last char to set
        _set.append([last_chars])
        setl += 1
    # add set to re
    for j, group in enumerate(_set): _set[j] = "".join(translater.get(c) or re_escape(c) for c in group)
    if len(_set) == 0: pass
    elif len(_set) == 1: reg += _set[0]
    else: reg += "(?:" + "|".join(_set) + ")"
    #_set[:], setl = (), 0

    # add retained to re
    for r in retained: reg += translater.get(r) or re_escape(r)
    #retained[:] = ()

    return reg

  #assert str_compilesearch("coucou", {}) == "coucou"
  #assert str_compilesearch("cœur" , {"c":"[cç]","ç":"[cç]","oe":"(?:oe|œ)","œ":"(?:oe|œ)"}) == "[cç](?:oe|œ)ur"
  #assert str_compilesearch("coeur", {"c":"[cç]","ç":"[cç]","oe":"(?:oe|œ)","œ":"(?:oe|œ)"}) == "[cç](?:oe|(?:oe|œ))ur"  # strange output but does work
  ##print(str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"}))
  #assert re.compile("^" + str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"}) + "$").match("abthvfficde")
  #assert re.compile("^" + str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"}) + "$").match("abᵺvﬃcde")
  #assert re.compile("^" + str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"}) + "$").match("abᵺ…ﬁcde")
  #assert re.compile("^" + str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"}) + "$").match("abtƕfﬁcde")
  ##print(re.compile(str_compilesearch("abthvfficde", {"th":"(?:th|ᵺ)","hv":"(?:hv|ƕ)","vf":"(?:vf|…)","ffi":"(?:ffi|ﬃ)","fi":"(?:fi|ﬁ)"})))
  #ascii_specs = _registry["default"]
  #print(re.compile(str_compilesearch("…", mk_translater(ascii_specs))))
  #print(re.compile(str_compilesearch("ha", mk_translater(ascii_specs))))
  #assert re.compile(str_compilesearch("ha", mk_translater(ascii_specs))).match("ハ")
  #print(re.compile(str_compilesearch("abthvfficde", mk_translater(ascii_specs))))
  #assert re.compile(str_compilesearch("abthvfficde", mk_translater(ascii_specs))).match("abtƕfﬁcde")
  #assert re.compile(str_compilesearch("abthvfficde", mk_translater(ascii_specs)), re.I).match("abtǶfﬁcde")
  ##assert re.compile(str_compilesearch("abthvfficde", mk_translater(ascii_specs, ignore_case=True))).match("abtǶfﬁcde")  # XXX NIY
  #assert re.compile(str_compilesearch("abtƕfﬁcde", mk_translater(ascii_specs))).match("abthvfficde")
  #assert re.compile(str_compilesearch("abtƕfﬁcde", mk_translater(ascii_specs))).match("abtƕfﬁcde")
  #print("ok!")

  def re_compilesearch(search, flags=0, *, translater=None):  #, *, ignore_case=False):  # use ignore_case for mk_translater param ?
    # XXX find a better name for `translater`
    if translater is None:
      if flags & re.I:
        if re_compilesearch._computed_case_insensitive_translater is None:
          re_compilesearch._computed_case_insensitive_translater = mk_translater(merge_keys_and_values({}, *re_compilesearch._registry.values(), lower_keys=True))  # XXX use re_compilesearch._mk_translater ?
        translater = re_compilesearch._computed_case_insensitive_translater
      else:
        if re_compilesearch._computed_translater is None:
          re_compilesearch._computed_translater = mk_translater(merge_keys_and_values({}, *re_compilesearch._registry.values()))  # XXX use re_compilesearch._mk_translater ?
        translater = re_compilesearch._computed_translater
    if flags & re.I: search = search.lower()
    return re.compile(re_compilesearch.str_compilesearch(search, translater), flags)

  re_compilesearch._registry = _registry
  re_compilesearch._computed_translater = None
  re_compilesearch._computed_case_insensitive_translater = None

  re_compilesearch.str_compilesearch = str_compilesearch
  re_compilesearch._mk_translater = mk_translater

  return re_compilesearch
re_compilesearch = re_compilesearch()
re_compilesearch._required_globals = ["re", "re_escape"]
