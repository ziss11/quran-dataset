import codecs
import json
import re


def load_json(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        data = json.load(f)

    return data


def create_json(dict_data, filename):
    with codecs.open(f'data/{filename}', 'w', 'utf-8') as f:
        f.write(json.dumps(dict_data, ensure_ascii=False))


def build_verses():
    quran_id_path = 'old/quran_id.json'
    quran_en_path = 'old/quran_en.json'
    tafsir_path = 'old/quran_with_tafsir.json'

    data_id = load_json(quran_id_path)
    data_en = load_json(quran_en_path)
    data_tafsir = load_json(tafsir_path)

    new_verses = list()
    pre_bismillah = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"

    for i, idn in enumerate(data_id):
        idn_verses = idn['verses']
        en_verses = data_en[i]['verses']
        tafsir = data_tafsir[i]['ayahs']

        new_data_list = list()
        for j, idn_verse in enumerate(idn_verses):
            tafsir_text = tafsir[j]['tafsir']['kemenag']['short']

            new_data = {'pre_bismillah': pre_bismillah,
                        'text': idn_verse['text'],
                        'translation': {
                            'idn': idn_verse['translation'],
                            'en': en_verses[j]['translation']},
                        'tafsir': {'id': tafsir_text}}
            new_data_list.append(new_data)

        verse_model = {'id': idn['id'], 'data': new_data_list}
        new_verses.append(verse_model)

    return new_verses


def build_surah():
    quran1_path = 'old/quran.json'
    quran2_path = 'old/quran_id.json'
    juz_path = 'old/juz.json'
    tafsir_path = 'old/quran_with_tafsir.json'

    surah1_json = load_json(quran1_path)
    surah2_json = load_json(quran2_path)
    juz_json = load_json(juz_path)
    data_tafsir = load_json(tafsir_path)

    unused_columns = ['recitation', 'place',
                      'number_of_surah', 'number_of_ayah']
    new_surah = list()

    for juz in juz_json:
        start = int(juz['start']['index'])
        end = int(juz['end']['index'])

        for i, surah1 in enumerate(surah1_json):
            desc = data_tafsir[i]['description']
            en_revelation = ''
            id_revelation = ''

            if surah1['place'] == 'Mecca':
                en_revelation = 'Mecca'
                id_revelation = 'Mekkah'
            elif surah1['place'] == 'Medina':
                en_revelation = 'Medina'
                id_revelation = 'Madinah'

            surah1['name'] = surah2_json[i]['transliteration']
            surah1['description'] = {'idn': desc}

            new = {'id': surah1['number_of_surah'],
                   'total_verse': surah1['number_of_ayah'],
                   'revelation': {'en': en_revelation, 'idn': id_revelation}}

            new.update(surah1)
            new_surah.append(new)

    for surah in new_surah:
        for column in unused_columns:
            surah.pop(column)

    return new_surah


def build_juz():
    juz_path = 'old/juz.json'
    surah_path = 'data/new_surah.json'

    juz_json = load_json(juz_path)
    surah_json = load_json(surah_path)

    new_juz = list()

    for juz in juz_json:
        start = int(juz['start']['index'])
        end = int(juz['end']['index'])

        selected_surah = [surah_json[i] for i in range(start-1, end)]

        start_verse = re.findall(r'[0-9]+', juz['start']['verse'])[0]
        end_verse = re.findall(r'[0-9]+', juz['end']['verse'])[0]

        juz_model = {'id': int(juz['index']),
                     'start_surah': selected_surah[0]['name'],
                     'start_verse': start_verse,
                     'end_surah': selected_surah[len(selected_surah)-1]['name'],
                     'end_verse': end_verse,
                     'surah': selected_surah}

        new_juz.append(juz_model)

    return new_juz


if __name__ == '__main__':
    dict_data = [build_juz(), build_surah(), build_verses()]
    saved_filename = ['new_juz.json', 'new_surah.json', 'new_verse.json']

    for data, filename in zip(dict_data, saved_filename):
        create_json(data, filename)
