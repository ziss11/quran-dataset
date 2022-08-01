import codecs
import json


def load_json(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        data = json.load(f)

    return data


def build_surah():
    quran1_path = 'old/quran.json'
    quran2_path = 'old/quran_id.json'

    data1 = load_json(quran1_path)
    data2 = load_json(quran2_path)

    unused_columns = ['recitation', 'place',
                      'number_of_surah', 'number_of_ayah']
    new_surah = list()

    en_revelation = ''
    id_revelation = ''

    for surah1, surah2 in zip(data1, data2):
        if surah1['place'] == 'Mecca':
            en_revelation = 'Mecca'
            id_revelation = 'Mekkah'
        elif surah1['place'] == 'Medina':
            en_revelation = 'Medina'
            id_revelation = 'Madinah'

        surah1['name'] = surah2['transliteration']

        new = {'id': surah1['number_of_surah'],
               'total_verse': surah1['number_of_ayah'],
               'revelation': {'en': en_revelation, 'id': id_revelation}}

        new.update(surah1)
        new_surah.append(new)

    for surah in new_surah:
        for column in unused_columns:
            surah.pop(column)

    return {'surah': new_surah}


def build_verses():
    quran_id_path = 'old/quran_id.json'
    quran_en_path = 'old/quran_en.json'

    data_id = load_json(quran_id_path)
    data_en = load_json(quran_en_path)

    new_verses = list()

    for idn, en in zip(data_id, data_en):
        idn_verses = idn['verses']
        en_verses = en['verses']

        for idn_verse, en_verse in zip(idn_verses, en_verses):
            verse_model = {'id': idn_verse['id'],
                           'text': idn_verse['text'],
                           'translation': {
                'idn': idn_verse['translation'],
                'en': en_verse['translation'],
            }}

            new_verses.append(verse_model)

    return {'verses': new_verses}


if __name__ == '__main__':
    surah = build_surah()
    verses = build_verses()

    with codecs.open('new/new_surah.json', 'w', 'utf-8') as f:
        f.write(json.dumps(surah, ensure_ascii=False))

    with codecs.open('new/new_verse.json', 'w', 'utf-8') as f:
        f.write(json.dumps(verses, ensure_ascii=False))
