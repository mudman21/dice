import streamlit as st
import json
import random


# JSON 파일 읽기
def load_words():
    try:
        with open('words.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 기본적으로 모든 카테고리를 포함하도록 보장
            if 'adverbs' not in data:
                data['adverbs'] = []
            if 'adjectives' not in data:
                data['adjectives'] = []
            if 'nouns' not in data:
                data['nouns'] = []
            if 'combinations' not in data:
                data['combinations'] = []
            return data
    except FileNotFoundError:
        return {'adverbs': [], 'adjectives': [], 'nouns': [], 'combinations': []}


# JSON 파일 저장
def save_words(data):
    with open('words.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 단어 추가 함수
def add_words(category, words):
    current_words = set(data[category])
    new_words = set(words)
    duplicates = new_words & current_words
    unique_words = new_words - current_words

    if duplicates:
        st.warning(f"중복된 단어: {', '.join(duplicates)}")

    data[category].extend(unique_words)
    save_words(data)

    return unique_words


# 단어 제거 함수
def remove_words(category, words):
    current_words = set(data[category])
    words_to_remove = set(words)
    if not words_to_remove <= current_words:
        return words_to_remove, False

    remaining_words = current_words - words_to_remove
    data[category] = list(remaining_words)
    save_words(data)

    return words_to_remove, True


# 초기 데이터 로드
data = load_words()

# 스트림릿 앱 제목 설정
st.title('단어 입력 인터페이스')

# 부사, 형용사, 명사 입력 필드 생성
adverb_input = st.text_input('부사 입력 (","로 구분)')
adjective_input = st.text_input('형용사 입력 (","로 구분)')
noun_input = st.text_input('명사 입력 (","로 구분)')

# 입력된 단어들을 ","로 구분하여 리스트로 변환
adverbs = [x.strip() for x in adverb_input.split(',')] if adverb_input else []
adjectives = [x.strip() for x in adjective_input.split(',')] if adjective_input else []
nouns = [x.strip() for x in noun_input.split(',')] if noun_input else []

# 입력된 단어를 JSON 형식으로 저장
if st.button('입력 확인 및 저장'):
    added_adverbs = add_words('adverbs', adverbs)
    added_adjectives = add_words('adjectives', adjectives)
    added_nouns = add_words('nouns', nouns)

    if added_adverbs:
        st.write('추가된 부사:', added_adverbs)
    if added_adjectives:
        st.write('추가된 형용사:', added_adjectives)
    if added_nouns:
        st.write('추가된 명사:', added_nouns)

    st.success('단어들이 성공적으로 저장되었습니다!')

# 단어 제거 기능
remove_category = st.selectbox('제거할 단어의 종류 선택', ['부사', '형용사', '명사', '조합'])
remove_words_input = st.text_input('제거할 단어 입력 (","로 구분)')

# 선택한 카테고리와 변수 매핑
category_map = {
    '부사': 'adverbs',
    '형용사': 'adjectives',
    '명사': 'nouns',
    '조합': 'combinations'
}

# 단어 제거
if st.button('단어 제거'):
    category = category_map[remove_category]
    words_to_remove = [x.strip() for x in remove_words_input.split(',')] if remove_words_input else []
    removed_words, success = remove_words(category, words_to_remove)

    if success:
        st.write('제거된 단어:', removed_words)
        st.success(f'{remove_category}에서 단어가 제거되었습니다.')
    else:
        st.warning(f'{remove_category}에서 제거할 단어가 존재하지 않습니다.')

# 부사 참여 확률 설정
adverb_probability = st.slider('부사 참여 확률', 0, 100, 50)

# 단어 랜덤 조합 기능
if 'random_combination' not in st.session_state:
    st.session_state.random_combination = ""
    st.session_state.random_adverb = ""
    st.session_state.random_adjective = ""
    st.session_state.random_noun = ""

if st.button('랜덤 조합'):
    if data['adverbs'] and data['adjectives'] and data['nouns']:
        st.session_state.random_adverb = random.choice(
            data['adverbs']) if random.random() < adverb_probability / 100 else ""
        st.session_state.random_adjective = random.choice(data['adjectives'])
        st.session_state.random_noun = random.choice(data['nouns'])

        st.session_state.random_combination = f"{st.session_state.random_adverb} {st.session_state.random_adjective} {st.session_state.random_noun}".strip()

        combination_html = f"""
        <p><span style="color: red;">{st.session_state.random_adverb}</span> 
        <span style="color: blue;">{st.session_state.random_adjective}</span> 
        <span style="color: green;">{st.session_state.random_noun}</span></p>
        """
        st.markdown(combination_html, unsafe_allow_html=True)
    else:
        st.warning('부사, 형용사, 명사를 모두 입력해 주세요.')

# 조합 저장 기능
if st.button('이 조합 저장'):
    if st.session_state.random_combination:
        if st.session_state.random_combination not in data['combinations']:
            data['combinations'].append(st.session_state.random_combination)
            save_words(data)
            st.success('랜덤 조합이 저장되었습니다!')
        else:
            st.warning('중복된 조합입니다!')

# 저장된 조합 랜덤 표시 기능
if st.button('저장된 조합 랜덤 표시'):
    if data['combinations']:
        random_saved_combination = random.choice(data['combinations'])
        st.write('저장된 랜덤 조합:', random_saved_combination)
    else:
        st.warning('저장된 조합이 없습니다.')

# 각 요소 복사 기능
if st.session_state.random_adverb:
    st.text_area('부사 복사', st.session_state.random_adverb)
if st.session_state.random_adjective:
    st.text_area('형용사 복사', st.session_state.random_adjective)
if st.session_state.random_noun:
    st.text_area('명사 복사', st.session_state.random_noun)

# JSON 파일 내용 출력
if st.button('JSON 파일 내용 보기'):
    st.json(data)
