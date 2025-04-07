import tkinter as tk
from PIL import ImageTk, Image
from routing import *
from start_station import *
from tkinter import messagebox

#--------- header start ---------

def route_repeat(course):
    # course는 사용자가 선택한 경로의 시작역과 모든 역의 정보가 담겨있음
    totalRoute = []
    totalShortestDist = 0
    for i in len(course):
        totalRoute.insert(shotestRoute(course[i], course[i + 1])[0])
        totalShortestDist += (shotestRoute(course[i], course[i + 1])[1])

start = None
end = None

def handle_search():
    global start, end

    input_text = search_entry.get().strip()

    if input_text == placeholder_text:
        messagebox.showwarning("입력 오류","검색할 역 이름을 입력하세요.")
        return

    if input_text not in stations:
        messagebox.showerror("역 없음", f"'{input_text}' 는(은) 존재하지 않는 역입니다.")
        return

    if start is None:
        start = input_text
        print(f"[출발역 설정] {start}")
        messagebox.showinfo("출발역 설정", f"출발역이 {start}로 설정되었습니다.")
        search_entry.delete(0, tk.END)
        search_entry.insert(0, placeholder_text)

root = tk.Tk()
root.geometry("1400x800")

header_frame = tk.Frame(root, height=60, background="#ffffff")
map_frame = tk.Frame(root, width=960, height=340, background="#ffffff")
list_frame = tk.Frame(root, width=960, height=340, background="#ffffff")
side_frame = tk.Frame(root, width=380, height=700, background="#ffffff")

img_path = "button.png" 
start_img = ImageTk.PhotoImage(Image.open(img_path).resize((60, 30)))

left_group = tk.Frame(header_frame, bg="white")
left_group.pack(side="left", padx=20, pady=10)

start_img_label = tk.Label(left_group, image=start_img, bg="white")
start_img_label.pack(side="left", padx=(0, 5))

triangle_icon = tk.Label(left_group, text="▶", font=("Arial", 14), fg="gray", bg="white")
triangle_icon.pack(side="left", padx=(0, 5))

search_frame = tk.Frame(left_group, bg="#f2e6f7")
search_frame.pack(side="left")

placeholder_text = "역을 입력하세요"

search_entry = tk.Entry(search_frame, font=("Arial", 12), bg="#f2e6f7", bd=0, relief="flat", highlightthickness=0)
search_entry.insert(0, placeholder_text)
search_entry.config(fg="gray")
search_entry.pack(side="left", ipady=6, padx=(10, 5))

def clear_placeholder(event):
    if search_entry.get() == placeholder_text:
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")

def set_placeholder(event):
    if search_entry.get().strip() == "":
        search_entry.insert(0, placeholder_text)
        search_entry.config(fg="gray")

search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", set_placeholder)

search_icon = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="#f2e6f7", bd=0, relief="flat", activebackground="#e0d5f0", cursor="hand2",command=handle_search)
search_icon.pack(side="left", padx=(5, 10))

brand_label = tk.Label(header_frame, text="DATEWAY", font=("Arial", 14, "bold"), bg="white")
brand_label.pack(side="right", padx=20)

#--------- header end ---------

#--------- map&sid start ---------

img_path = r"C:\python\map.png"
gif_path = r"C:\python\kakao2.gif"
print("이미지 파일 경로:", img_path)


try:
    map_img = ImageTk.PhotoImage(Image.open(img_path).resize((960, 340), Image.LANCZOS))
    tk.Label(map_frame, image=map_img, bg="#ffffff").place(x=0, y=0)
except Exception:
    pass

try:
    gif = Image.open(gif_path)
    gif_frames = []

    for i in range(gif.n_frames):  # 모든 프레임 저장
        gif.seek(i)
        gif_frames.append(ImageTk.PhotoImage(gif.copy()))

    gif_label = tk.Label(side_frame)
    gif_label.place(x=0, y=0)

    def update_gif(index=0):
        gif_label.config(image=gif_frames[index])
        root.after(100, update_gif, (index + 1) % len(gif_frames))  # 100ms마다 프레임 변경

    update_gif()
except Exception as e:
    print("GIF 로드 오류:", e)

#--------- map&sid end ---------

#--------- list start ---------

places = [
    {'디큐브시티': {'station': '신도림', 'time': '10:30-20:30', 'loc': '서울 구로구 신도림동 692'}},
    {'타임스퀘어': {'station': '영등포', 'time': '10:30-22:00', 'loc': '서울 영등포구 영등포동4가 442'}},
    {'이촌 한강공원': {'station': '노량진', 'time': '연중무휴', 'loc': '서울 용산구 이촌동 302-17'}},
    {'서울로7017': {'station': '서울', 'time': '연중무휴', 'loc': '서울 중구 봉래동2가 122-14'}},
    {'덕수궁 돌담길+정동길': {'station': '시청', 'time': '11:00-14:00', 'loc': '서울 중구 정동 4'}},
    {'젊음의 거리': {'station': '종각', 'time': '연중무휴', 'loc': '서울 종로구 종로8길 5-8 구두수선대'}},
    {'광장시장': {'station': '종로5가', 'time': '09:00-18:00', 'loc': '서울 종로구 창경궁로 88'}},
    {'동대문디자인플라자': {'station': '동대문', 'time': '10:00-20:00', 'loc': '서울 중구 을지로 281'}},
    {'홍릉수목원': {'station': '청량리', 'time': '09:00-18:00', 'loc': '서울 동대문구 회기로 57'}},
    {'경희대 캠퍼스': {'station': '회기', 'time': '연중무휴', 'loc': '서울 동대문구 경희대로 26'}},
    {'광명동굴': {'station': '광명', 'time': '09:00-18:00', 'loc': '경기 광명시 가학로85번길 142'}},
    {'항동기찻길': {'station': '오류동', 'time': '연중무휴', 'loc': '서울 구로구 오리로 1189'}},
    {'전곡리유적': {'station': '연천', 'time': '연중무휴', 'loc': '경기 연천군 전곡읍 양연로 1510'}},
    {'한국만화박물관': {'station': '부천', 'time': '10:00-18:00', 'loc': '경기 부천시 원미구 길주로 1'}},
    {'안양예술공원': {'station': '안양', 'time': '연중무휴', 'loc': '경기 안양시 만안구 예술공원로131번길 7'}},
    {'화성행궁': {'station': '수원', 'time': '09:00-18:00', 'loc': '경기 수원시 팔달구 정조로 825'}},
    {'물향기수목원': {'station': '오산', 'time': '09:00-18:00', 'loc': '경기 오산시 청학로 211'}},
    {'왕송호수': {'station': '의왕', 'time': '연중무휴', 'loc': '경기 의왕시 초평동'}},
    {'인천차이나타운': {'station': '인천', 'time': '연중무휴', 'loc': '인천 중구 차이나타운로26번길 12-17'}},
    {'G밸리몰': {'station': '구로', 'time': '11:00-21:30', 'loc': '서울 금천구 디지털로10길 9 현대시티아울렛 5'}},
    {'진위천 유원지': {'station': '평택', 'time': '09:00-21:00', 'loc': '경기 평택시 진위면 진위서로 264-15'}},
    {'독립기념관': {'station': '천안', 'time': '09:30-18:00', 'loc': '충남 천안시 동남구 목천읍 독립기념관로 1 독립기념관'}},
    {'가을단풍길': {'station': '신도림', 'time': '연중무휴', 'loc': '서울 구로구 신도림동 328-34'}},
    {'문래창작촌': {'station': '영등포', 'time': '연중무휴', 'loc': '문래동3가 54-39'}},
    {'남산서울타워': {'station': '서울', 'time': '10:00-22:30', 'loc': '서울 용산구 용산동2가 산1-3'}},
    {'서울시립미술관': {'station': '시청', 'time': '10:00-20:00', 'loc': '서울 중구 서소문동 37'}},
    {'인사동': {'station': '종각', 'time': '연중무휴', 'loc': '서울 종로구 인사동'}},
    {'청계천': {'station': '종로5가', 'time': '연중무휴', 'loc': '서울 종로구 창신동'}},
    {'혜화동': {'station': '동대문', 'time': '연중무휴', 'loc': '서울특별시 종로구 혜화동'}},
    {'회기 파전골목': {'station': '회기', 'time': '연중무휴', 'loc': '서울 동대문구 회기로28길 8'}},
    {'호봉골': {'station': '광명', 'time': '연중무휴', 'loc': '경기 광명시 일직동'}},
    {'오류동역광장': {'station': '오류동', 'time': '연중무휴', 'loc': '서울 구로구 오류동 65-6'}},
    {'연천회관': {'station': '연천', 'time': '09:00-21:00', 'loc': '경기 연천군 연천읍 평화로1219번길 42'}},
    {'부천중앙공원': {'station': '부천', 'time': '연중무휴', 'loc': '경기 부천시 원미구 소향로 162'}},
    {'중앙시장': {'station': '안양', 'time': '10:00-20:00', 'loc': '경기 안양시 만안구 냉천로 196 중앙시장'}},
    {'방화수류정': {'station': '수원', 'time': '연중무휴', 'loc': '경기 수원시 팔달구 수원천로392번길 44-6 방화수류정'}},
    {'오산천': {'station': '오산', 'time': '연중무휴', 'loc': '경기 오산시 누읍동 1'}},
    {'철도박물관': {'station': '의왕', 'time': '09:00-18:00', 'loc': '경기 의왕시 철도박물관로 142 철도박물관'}},
    {'월미도': {'station': '인천', 'time': '10:00-21:00', 'loc': '인천 중구 북성동1가 98-352'}},
    {'안양천 벚꽃길': {'station': '구로', 'time': '연중무휴', 'loc': '경기 군포시 당정동'}},
    {'소사벌 카페거리': {'station': '평택', 'time': '연중무휴', 'loc': '경기도 평택시 평남로 일대'}},
    {'태조산공원': {'station': '천안', 'time': '09:00-21:00', 'loc': '충남 천안시 동남구 태조산길 261 태조산청소년수련관'}},
    {'경복궁': {'station': '경복궁', 'time': '09:00-18:00', 'loc': '서울 종로구 사직로 161 경복궁'}},
    {'북촌 한옥마을': {'station': '안국', 'time': '10:00-17:00', 'loc': '서울 종로구 계동길 37'}},
    {'서촌 쭈먹': {'station': '경복궁', 'time': '11:00-22:00', 'loc': '서울 종로구 자하문로1길 20'}},
    {'신사동 가로수길': {'station': '신사', 'time': '00:00-24:00', 'loc': '서울 강남구 신사동'}},
    {'K-star road': {'station': '압구정', 'time': '00:00-24:00', 'loc': '서울 강남구 압구정동 394'}},
    {'장독대': {'station': '학여울', 'time': '11:00-22:00', 'loc': '서울 강남구 영동대로 221 서림상가 뒷편1층 1호'}},
    {'압구정샌드위치': {'station': '대치', 'time': '08:00-20:00', 'loc': '서울 강남구 삼성로 212 은마종합상가 지하1층 A동 62호'}},
    {'남산공원': {'station': '충무로', 'time': '00:00-24:00', 'loc': '강원 강릉시 노암동 740-1'}},
    {'서울경마공원': {'station': '수서', 'time': '09:30-18:00', 'loc': '경기 과천시 경마공원대로 107'}},
    {'세빛섬': {'station': '고속터미널', 'time': '00:00-24:00', 'loc': '서울특별시 서초구 올림픽대로 2085-14 세빛섬'}},
    {'둘리뮤지엄': {'station': '쌍문', 'time': '10:00-18:00', 'loc': '서울 도봉구 시루봉로1길 6'}},
    {'북서울꿈의숲': {'station': '미아', 'time': '00:00-24:00', 'loc': '서울 강북구 월계로 173'}},
    {'이화벽화마을': {'station': '혜화', 'time': '00:00-24:00', 'loc': '서울 종로구 이화장길 70-11'}},
    {'동대문DDP': {'station': '동대문역사공원', 'time': '10:00-20:00', 'loc': '서울 중구 을지로 281'}},
    {'남산골한옥마을': {'station': '명동', 'time': '09:00-20:00', 'loc': '서울 중구 퇴계로34길 28 남산골한옥마을'}},
    {'숭례문': {'station': '회현', 'time': '09:00-18:00', 'loc': '서울 중구 세종대로 40'}},
    {'서울로7017': {'station': '서울', 'time': '00:00-24:00', 'loc': '서울 중구 청파로 432'}},
    {'전쟁기념관': {'station': '삼각지', 'time': '09:30-18:00', 'loc': '서울 용산구 이태원로 29'}},
    {'국립중앙박물관': {'station': '이촌', 'time': '10:00-18:00', 'loc': '서울 용산구 서빙고로 137 국립중앙박물관'}},
    {'창경궁': {'station': '혜화', 'time': '09:00-21:00', 'loc': '서울 종로구 창경궁로 185 창경궁'}},
    {'남대문시장': {'station': '회현', 'time': '00:00-23:00', 'loc': '서울 중구 남대문시장4길 21'}},
    {'국립서울현충원': {'station': '동작', 'time': '06:00-18:00', 'loc': '서울 동작구 현충로 210'}},
    {'서울 하늘공원': {'station': '월드컵경기장', 'time': '07:00-18:00', 'loc': '서울 마포구 하늘공원로 95'}},
    {'난지캠핑장': {'station': '월드컵경기장', 'time': '00:00-24:00', 'loc': '서울 마포구 한강난지로 28'}},
    {'이태원 세계 음식 거리': {'station': '이태원', 'time': '00:00-24:00', 'loc': '서울 용산구 이태원동'}},
    {'경리단길': {'station': '녹사평', 'time': '00:00-24:00', 'loc': '서울 용산구 이태원동'}},
    {'동묘구제시장': {'station': '동묘앞', 'time': '00:00-24:00', 'loc': '서울 종로구 숭인동 102-8'}},
    {'보문사': {'station': '보문', 'time': '08:00-17:00', 'loc': '서울 성북구 보문사길 20 보문사'}},
    {'블루스퀘어': {'station': '한강진', 'time': '00:00-24:00', 'loc': '서울 용산구 이태원로 294'}},
    {'공트럴파크': {'station': '태릉입구', 'time': '00:00-24:00', 'loc': '서울 노원구 화랑로 475-6'}}
]

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(list_frame, bg="#ffffff", yscrollcommand=scrollbar.set, width=960, height=340)
canvas.pack(side="left", fill="both", expand=True)

scrollbar.config(command=canvas.yview)

places_frame = tk.Frame(canvas, bg="#ffffff", width=960, height=340, pady=40)
canvas.create_window((0, 0), window=places_frame, anchor="nw")

course = []

# 카드 클릭시 역 가져오기
def get_courses(station):
    global idx, course
    print(f" 선택된 역: {station}")

    if station in course:
  
        course.remove(station)
        print(f"중복 선택 → '{station}' 삭제됨")
    else:
       
        course.append(station)

    print(f"[현재 경로] {course}")
    print('')

# 장소카드 클릭이벤트 함수
def click_place(station, title): 
    get_courses(station)

# # 장소카드 호버효과
# def on_enter(event):
#     place_card.config(bg="#eeeeee")

# def on_leave(event):
#     place_card.config(bg="#ffffff")

for i, place in enumerate(places):
    if i % 3 == 0:
        wrap = tk.Frame(places_frame, bg="#ffffff")
        wrap.pack(padx=4, pady=10)

    # 장소 카드 영역 생성
    place_card = tk.Frame(wrap, width=300, height=100, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1, cursor="hand2")
    place_card.pack_propagate(0)  # pack_propagate(0) 자동으로 사이즈 조절되는 기능 끄기
    place_card.pack(side="left", fill="y", padx=10)
    # 호버효과, 마지막 위젯만 호버됨
    # place_card.bind("<Enter>", on_enter)
    # place_card.bind("<Leave>", on_leave)

    # 이미지 넣기
    image = Image.open(f"./images/{(i+1)}.png")
    image = image.resize((90, 90))
    resized_image = ImageTk.PhotoImage(image)

    image_area = tk.Label(place_card, image=resized_image, bg="#ffffff")
    image_area.image = resized_image # 이미지 객체를 유지할 수 있도록 참조를 저장
    image_area.pack(side='left', padx=5, pady=5)
    
    # 장소 이름 넣기
    for title in place.keys():
        place_title = tk.Label(place_card, text=title, bg="#ffffff", font=("",10,"bold"))
        place_title.pack(side="top", anchor="w", pady=8)

        place_time = tk.Label(place_card, text="운영시간: "+place[title]['time'], bg="#ffffff")
        place_time.pack(side="top", anchor="w")
        
        place_location = tk.Label(place_card, text="위치: "+place[title]['loc'], bg="#ffffff", wraplength="180", justify="left")
        place_location.pack(side="top", anchor="w")

        place_card.bind('<Button-1>', lambda _, station=place[title]['station'], title=title: click_place(station,title))
        image_area.bind('<Button-1>', lambda _, station=place[title]['station'], title=title: click_place(station,title))
        place_title.bind('<Button-1>', lambda _, station=place[title]['station'], title=title: click_place(station,title))
        place_time.bind('<Button-1>', lambda _, station=place[title]['station'], title=title: click_place(station,title))
        place_location.bind('<Button-1>', lambda _, station=place[title]['station'], title=title: click_place(station,title))

places_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

#--------- list end ---------

header_frame.pack(side="top", fill="x")
map_frame.place(x=20, y=80)
list_frame.place(x=20, y=440)
side_frame.place(x=1000, y=80)

root.mainloop()