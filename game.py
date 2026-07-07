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
            st.session_state.message = f"🏃 무사히 도망쳤습니다! (현재 {st.session_state.turns}턴 생존 중)"
    else:
        st.session_state.message = "⚠️ 벽에 막혀서 그쪽으로 갈 수 없습니다. 다른 방향을 선택하세요!"

# 5. 게임 보드(그리드) 렌더링 함수
def render_grid():
    grid_str = ""
    for y in range(GRID_SIZE):
        row_str = ""
        for x in range(GRID_SIZE):
            if [x, y] == st.session_state.player_pos and [x, y] == st.session_state.tagger_pos:
                row_str += "💥 " # 잡힌 상태
            elif [x, y] == st.session_state.player_pos:
                row_str += "🏃 " # 플레이어
            elif [x, y] == st.session_state.tagger_pos:
                row_str += "👹 " # 술래
            else:
                row_str += "⬜ " # 빈 공간
        grid_str += f"### {row_str}\n"
    return grid_str

# 6. 화면 출력 영역
# 상태 메시지 및 점수
if st.session_state.game_over:
    st.error(st.session_state.message)
else:
    st.info(st.session_state.message)

st.metric(label="🏆 생존 턴 수", value=f"{st.session_state.turns} 턴")

# 맵 출력 (가운데 정렬 느낌으로 배치)
col_board_1, col_board_2, col_board_3 = st.columns([1, 2, 1])
with col_board_2:
    st.markdown(render_grid())

st.write("---")

# 7. 조작 버튼 (방향키 컨트롤러 레이아웃)
if not st.session_state.game_over:
    st.write("### 🎮 이동 방향 선택")
    c1, c2, c3 = st.columns(3)
    
    with c2:
        if st.button("⬆️ 위로", use_container_width=True):
            move_player(0, -1)
            st.rerun()
            
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("⬅️ 왼쪽", use_container_width=True):
            move_player(-1, 0)
            st.rerun()
    with c5:
        if st.button("⬇️ 아래로", use_container_width=True):
            move_player(0, 1)
            st.rerun()
    with c6:
        if st.button("➡️ 오른쪽", use_container_width=True):
            move_player(1, 0)
            st.rerun()
else:
    # 게임 오버 시 재시작 버튼 출력
    if st.button("🔄 게임 다시 시작하기", type="primary", use_container_width=True):
        init_game()
        st.rerun()
