import pygame
import os, sys
import ug_simul

# exe파일로 가공하기 위해 파일 환경변수 설정(이미지 파일)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS                    # 임시로 제공되는 폴더의 경로
    except Exception:
        # sys._MEIPASS is not defined, so use the original path
        # 현재 경로를 절대경로로 바꿔서 반환, 도트 표시는 현재 디렉토리에서 절대경로
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
icon = pygame.image.load(resource_path("images/lostark_icon.ico"))
pygame.display.set_icon(icon)

# RGB 값을 전역변수로 만든 후 포맷, rect 색상 설정시 RGB 코드 대신 색상으로 입력 가능
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

# 윈도우 스크린 사이즈 설정
size = [1024, 768]
screen = pygame.display.set_mode(size)

# 글씨체 및 크기 설정
font = pygame.font.SysFont('malgungothic', 40, True)

# ug_simul.py의 upgrade_Simul() 클래스 호출
us = ug_simul.upgrade_Simul()

# 커스텀 모드의 화살표 클릭시 증감되는 값을 화면에 보여주기 위한 변수 선언 및 초기화
cus_lv = 0
scene_chk = 0


# 윈도우 화면에 글자를 사용하기 위한 함수 (출력할 내용, 글자의 X좌표, 글자의 Y좌표, 글자색)
def printText(contents_text, text_x, text_y, text_color):
    textSurfaceObj = font.render(contents_text, True, text_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (text_x, text_y)
    screen.blit(textSurfaceObj, textRectObj)

# rect와 printText 함수를 사용해 버튼을 만드는 함수 (rect색상, rect x좌표, rect y좌표, 버튼 x축 길이, 버튼 y축 길이, 버튼 글자내용, 글자색)
def make_Button(btn_color, btn_x_pos, btn_y_pos, btn_x_size, btn_y_size, contents_text, text_color):
    pygame.draw.rect(screen, btn_color, pygame.Rect(btn_x_pos, btn_y_pos, btn_x_size, btn_y_size))
    printText(contents_text, btn_x_pos + (btn_x_size / 2), btn_y_pos + (btn_y_size / 2), text_color)


pygame.display.set_caption("강화 시뮬레이션")  # 캡션 설정
# 화면 초당 프레임 횟수 선언 변수

done = False
clock = pygame.time.Clock()


def main_scene():                   # 초기화면 구현
    bg_image = pygame.image.load(resource_path("images/background_main.png"))
    screen.blit(bg_image, (0, 0))  # 이미지 그리기
    make_Button((105, 0, 0), 100, 600, 300, 100, '일반모드', WHITE)
    make_Button((105, 0, 0), 624, 600, 300, 100, '커스텀모드', WHITE)
    pygame.draw.circle(screen, WHITE, (55, 55), 20)
    printText('?', 55, 55, BLACK)
    us.reset_var()
    return 0

def nor_scene():
    screen.fill((36, 36, 36))  # 함수 실행시 기존 화면을 지워주기 위해 실행
    # 버튼 생성 부분
    make_Button((105, 0, 0), 362, 600, 300, 100, '강화시작', WHITE)
    make_Button((105, 0, 0), 954, 20, 50, 50, '←', WHITE)
    return 1


def cus_scene():
    screen.fill((36, 36, 36))  # 함수 실행시 기존 화면을 지워주기 위해 실행
    # 버튼 생성 부분
    make_Button((105, 0, 0), 362, 600, 300, 100, '강화시작', WHITE)
    make_Button((105, 0, 0), 362, 500, 50, 50, '<', WHITE)
    make_Button((105, 0, 0), 612, 500, 50, 50, '>', WHITE)
    make_Button((105, 0, 0), 954, 20, 50, 50, '←', WHITE)
    return 2


main_scene()  # 메인 화면 호출

while not done:
    clock.tick(10)  #pygame.time.Clock()을 선언한 clock 함수를 통해 초당 프레임 설정

    # 메인 이벤트 루프
    for event in pygame.event.get():        # 이벤트 발생을 인지하는 함수
        mouse_pos = pygame.mouse.get_pos()  # 마우스 좌표 값 획득
        mouse_x = mouse_pos[0]              # 마우스 x축 좌표 값 획득
        mouse_y = mouse_pos[1]              # 마우스 y축 좌표 값 획득
        if event.type == pygame.QUIT:       # 이벤트 함수가 pygame.QUIT 이라는 값과 일치하는지 검사하는 라인
                                            # GUI창에서 X버튼을 누르면 발생하는 이벤트
            done = True                     # while문 종료
        # 메인화면 부분
        if scene_chk == 0:
            if event.type == pygame.MOUSEMOTION:
                if 75 >= mouse_x >= 35 and 75 >= mouse_y >=35:
                    make_Button(WHITE, 80, 35, 600, 400, 'TEST', BLACK)
                    tutorial_image = pygame.image.load(resource_path("images/tutorial_image.png"))
                    screen.blit(tutorial_image, (80, 35))  # 이미지 그리기
                else:
                    main_scene()

            if event.type == pygame.MOUSEBUTTONUP:      # 일반모드 선택시
                if 400 >= mouse_x >= 100 and 700 >= mouse_y >= 600:
                    nor_scene()
                    scene_chk = nor_scene()
                    ug_lv, per_wei_success = us.nor_mode()
                    printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                    printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)
                    pygame.time.delay(300)

            if event.type == pygame.MOUSEBUTTONUP:      # 커스텀모드 선택시
                if 924 >= mouse_x >= 624 and 700 >= mouse_y >= 600:
                    cus_lv = 1
                    cus_scene()
                    scene_chk = cus_scene()
                    ug_lv, per_wei_success = us.cus_mode(cus_lv)
                    print(ug_lv, per_wei_success)
                    printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                    printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)
                    printText(str(cus_lv), 512, 525, WHITE)
                    pygame.time.delay(300)
        # 일반모드 부분
        elif scene_chk == 1:                                      # 일반모드 진입후 버튼누르면 수행
            if event.type == pygame.MOUSEBUTTONUP:              # 일반모드 선택시
                if 1004 >= mouse_x >= 954 and 70 >= mouse_y >= 20:
                    scene_chk = main_scene()
                    print('메인버튼 누름', scene_chk)

                if 662 >= mouse_x >= 362 and 700 >= mouse_y >= 600:           # 강화 시작 버튼 이미지가 들어간 x, y 좌표값 범위
                    try:
                        print("강화시작 누름")
                        nor_scene()
                        ug_result, ug_lv, per_wei_success, fail_cnt, jangin = us.upgrade_start()
                        print(ug_result, ug_lv, per_wei_success / 10, fail_cnt)
                        printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                        printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)
                        if jangin >= 1000:
                            jangin = 1000
                        printText("장인의 기운 : " + str(round(jangin / 10, 2)) + '%', 512, 300, WHITE)
                        printText(ug_result, 512, 400, WHITE)
                        printText("실패 횟수 : " + str(fail_cnt), 512, 500, WHITE)

                    except (AttributeError, TypeError):
                        printText("강화 단계 : 25", 300, 100, WHITE)
                        printText('강화 최대치 입니다', 512, 300, WHITE)

                    except Exception as e:
                        printText("오류 발생 : " + e)


        # 커스텀 모드 부분
        elif scene_chk == 2:                                      # 커스텀모드 진입후 버튼 누르면 수행
            if event.type == pygame.MOUSEBUTTONUP:              # 커스텀모드 선택시
                if 1004 >= mouse_x >= 954 and 70 >= mouse_y >= 20:
                        scene_chk = main_scene()
                        print('메인버튼 누름', scene_chk)

                if 662 >= mouse_x >= 362 and 700 >= mouse_y >= 600:      # 강화 시작 버튼 이미지가 들어간 x, y 좌표값 범위
                    try:
                        print("강화시작 누름")
                        cus_scene()
                        ug_result, ug_lv, per_wei_success, fail_cnt, jangin = us.upgrade_start()
                        printText(str(cus_lv), 512, 525, WHITE)
                        print(ug_result, ug_lv, per_wei_success / 10, fail_cnt)
                        printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                        printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)
                        if jangin >= 1000:
                            jangin = 1000
                        printText("장인의 기운 : " + str(round(jangin / 10, 2)) + '%', 512, 200, WHITE)
                        printText(ug_result, 512, 300, WHITE)
                        printText("실패 횟수 : " + str(fail_cnt), 512, 450, WHITE)

                    except (AttributeError, TypeError):                 # 강화 최대치 달성 시 발생하는 오류를 이용해 최대치 글자 출력
                        printText("강화 단계 : 25", 300, 100, WHITE)
                        printText('강화 최대치 입니다', 512, 300, WHITE)

                    except Exception as e:                              # 강화 최대치 이외 오류 발생시 오류 내용 출력
                        printText("오류 발생 : " + e)

                # 커스텀 모드 강화 단계 조정 부분
                if 412 >= mouse_x >= 362 and 600 >= mouse_y >= 500:
                    cus_scene()
                    print("< 누름")
                    cus_lv -= 1
                    if cus_lv < 1:                          # 강화 단계가 1단계 아래일시 더 이상 내려가지 않게 조정
                        cus_lv = 1
                    printText(str(cus_lv), 512, 525, WHITE)
                    ug_lv, per_wei_success = us.cus_mode(cus_lv)
                    print(ug_lv, per_wei_success)
                    printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                    printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)

                if 662 >= mouse_x >= 612 and 600 >= mouse_y >= 500:
                    cus_scene()
                    print("> 누름")
                    cus_lv += 1
                    if cus_lv > 24:                          # 강화 단계가 24단계 이상일시 더 이상 올라가지 않게 조정
                        cus_lv = 24
                    printText(str(cus_lv), 512, 525, WHITE)
                    ug_lv, per_wei_success = us.cus_mode(cus_lv)
                    print(ug_lv, per_wei_success)
                    printText("강화 단계 : " + str(ug_lv), 300, 100, WHITE)
                    printText("성공 확률 : " + str(per_wei_success / 10) + '%', 674, 100, WHITE)

    pygame.display.update()               # 행위 업데이트
