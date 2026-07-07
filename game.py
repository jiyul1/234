import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="텍스트 술래잡기 게임", page_icon="🏃", layout="centered")

st.title("🏃 텍스트 기반 술래잡기 게임")
st.markdown("**규칙:** 당신(🏃)은 술래(👹)를 피해 5x5 격자 안에서 도망쳐야 합니다. 상하좌우 버튼을 눌러 최대한 오래 살아남으세요!")
st.write("---")

# 2. 게임 초기화 및 상태 관리 (Session State)
GRID_SIZE = 5

def init_game():
    st.session_state.player_pos = [0, 0]
    # 술래는 플레이어와 겹치지 않는 곳에 랜덤 생성
    while True:
        tagger_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
        if tagger_pos != st.session_state.player_pos:
            st.session_state.tagger_pos = tagger_pos
            break
    st.session_state.turns = 0
    st.session_state.game_over = False
    st.session_state.message = "게임이 시작되었습니다! 도망칠 방향을 선택하세요."

if 'player_pos' not in st.session_state:
    init_game()

# 3. 인공지능 술래 이동 로직 (플레이어와 가장 가까운 방향으로 1칸 이동)
def move_tagger():
    px, py = st.session_state.player_pos
    tx, ty = st.session_state.tagger_pos
    
    possible_moves = []
    if tx < px: possible_moves.append([tx + 1, ty])
    elif tx > px: possible_moves.append([tx - 1, ty])
    if ty < py: possible_moves.append([tx, ty + 1])
    elif ty > py: possible_moves.append([tx, ty - 1])
    
    if possible_moves:
        # X축과 Y축 둘 다 이동 가능할 경우 랜덤으로 한 방향 선택
        st.session_state.tagger_pos = random.choice(possible_moves)

# 4. 플레이어 이동 및 턴 진행 로직
def move_player(dx, dy):
    if st.session_state.game_over:
        return

    new_x = st.session_state.player_pos[0] + dx
    new_y = st.session_state.player_pos[1] + dy

    # 맵 밖으로 벗어나지 않는지 확인
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        st.session_state.player_pos = [new_x, new_y]
        st.session_state.turns += 1
        
        # 플레이어 이동 후 술래와 만났는지 확인
        if st.session_state.player_pos == st.session_state.tagger_pos:
            st.session_state.game_over = True
            st.session_state.message = f"💥 앗! 이동한 곳에 술래가 있었습니다! (버틴 턴 수: {st.session_state.turns})"
            return

        # 술래 이동
        move_tagger()
        
        # 술래 이동 후 플레이어를 잡았는지 확인
        if st.session_state.player_pos == st.session_state.tagger_pos:
            st.session_state.game_over = True
            st.session_state.message = f"👹 술래에게 잡혔습니다! 게임 오버! (버틴 턴 수: {st.session_state.turns})"
        else:
            st.session_state.
