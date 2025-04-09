import tkinter as tk
from PIL import ImageTk, Image
from places import *
from routing import *
from start_station import *
from stations_coordinate import *
from tkinter import messagebox

root = tk.Tk()
root.geometry("1386x800")
root.resizable(False, False)

header_frame = tk.Frame(root, height=60, background="#ffffff")
map_frame = tk.Frame(root, width=960, height=340, background="#ffffff")
list_frame = tk.Frame(root, width=960, height=340, background="#ffffff")
side_frame = tk.Frame(root, width=366, height=700, background="#ffffff")

#--------- map start ---------

map_img_path = "map.png"
map = tk.Canvas(map_frame, width=960, height=340)
map.pack()
map_img = ImageTk.PhotoImage(Image.open(map_img_path).resize((960, 340)))
map.create_image(480, 170, image=map_img)

#--------- map end ---------

#--------- header start ---------

course = []
marker_img = tk.PhotoImage(file="start_marker.png")

def route_repeat(course):
    # 경로 초기화 코드
    global map_img_path
    map.delete("all")
    map_img = ImageTk.PhotoImage(Image.open(map_img_path).resize((960, 340)))
    map.create_image(480, 170, image=map_img)
    # 경로 초기화 코드
    course_color_idx = 0
    station_color_idx = 0
    course_color = ["red","yellow","green","blue"]
    station_color = ["lightcoral","cornsilk","greenyellow","dodgerblue"]
    
    totalRoute = []
    totalShortestDist = 0
    
    for i in range(len(course) - 1):
        route = list(shotestRoute(course[i], course[i + 1])[0])
        totalRoute += route
        totalShortestDist += (shotestRoute(course[i], course[i + 1])[1])


        for station in route:
            map.create_oval(stations_coordinate[station][0]-6,stations_coordinate[station][1]-6,stations_coordinate[station][0]+3,stations_coordinate[station][1]+3,fill=station_color[station_color_idx % 4])
        
        station_color_idx += 1

    for i in range(len(course)):
        map.create_oval(stations_coordinate[course[i]][0]-8,stations_coordinate[course[i]][1]-8,stations_coordinate[course[i]][0]+5,stations_coordinate[course[i]][1]+5,fill=course_color[course_color_idx % 4])
        course_color_idx += 1

    print("totalRoute: ", totalRoute)
    print("totalShortestDist: ", totalShortestDist)
    

start = None

def handle_search():
    global start, placeholder_text, course
    course = []

    input_text = search_entry.get().strip()

    if input_text == placeholder_text:
        messagebox.showwarning("입력 오류", "")
        return

    if input_text not in stations:
        messagebox.showerror("역 없음", f"'{input_text}' 는(은) 존재하지 않는 역입니다.")
        # 경로 초기화 코드
        global map_img_path
        map.delete("all")
        map_img = ImageTk.PhotoImage(Image.open(map_img_path).resize((960, 340)))
        map.create_image(480, 170, image=map_img)
        # 경로 초기화 코드
        return
    
    if start is not input_text:
        start = input_text
        course.insert(0, start)

    
    if start in course[1:]:
        course.remove(start)

    print(f"[출발역 설정] {start}")
    messagebox.showinfo("출발역 설정", f"출발역이 {start}로 설정되었습니다.")
    search_entry.delete(0, tk.END)
    search_entry.config(fg="black")
    route_repeat(course)
        
autocomplete_listbox = None
autocomplete_matches = []
autocomplete_index = -1

# 초성 포함 검색 기능
def cho_hangul_match(query, target):
    # 초성 매칭 간단한 버전 (full 정교한 건 라이브러리 필요)
    return query in target

def show_autocomplete(event):
    global autocomplete_listbox, autocomplete_matches, autocomplete_index
    
    # 방향키 이동/엔터 입력 시 자동완성 다시 뜨는 것 방지
    if event.keysym in ["Up", "Down", "Return"]:
        return

    typed = search_entry.get().strip()
    autocomplete_index = -1

    if autocomplete_listbox:
        autocomplete_listbox.destroy()

    if typed == "" or typed == placeholder_text:
        return

    # 포함/초성/시작 검색
    autocomplete_matches = [s for s in stations if typed in s]

    if autocomplete_matches:
        autocomplete_listbox = tk.Listbox(root, height=min(6, len(autocomplete_matches)), font=("Arial", 11),bg="#ffffff", relief="solid", bd=1)

        # Entry 바로 아래 좌표 계산
        x = search_entry.winfo_rootx() - root.winfo_rootx()
        y = search_entry.winfo_rooty() - root.winfo_rooty() + search_entry.winfo_height()
        w = search_entry.winfo_width()

        autocomplete_listbox.place(x=x, y=y, width=w)

        for match in autocomplete_matches:
            autocomplete_listbox.insert("end", match)

        autocomplete_listbox.bind("<ButtonRelease-1>", select_autocomplete_from_click)

def select_autocomplete_from_listbox():
    global autocomplete_listbox, autocomplete_matches

    if autocomplete_listbox and autocomplete_listbox.curselection():
        index = autocomplete_listbox.curselection()[0]
        selected = autocomplete_matches[index]
        update_search_entry(selected)

def update_search_entry(selected_text):
    global autocomplete_listbox
    search_entry.delete(0, tk.END)
    search_entry.insert(0, selected_text)
    search_entry.config(fg="black")
    search_entry.focus_set()
    if autocomplete_listbox:
        autocomplete_listbox.destroy()
        autocomplete_listbox = None

def handle_keypress(event):
    global autocomplete_index

    if not autocomplete_listbox:
        return

    autocomplete_listbox.focus_set()
    
    if event.keysym == "Down":
        autocomplete_index += 1
        if autocomplete_index >= autocomplete_listbox.size():
            autocomplete_index = 0
        autocomplete_listbox.select_clear(0, "end")
        autocomplete_listbox.select_set(autocomplete_index)
        autocomplete_listbox.activate(autocomplete_index)

    elif event.keysym == "Up":
        autocomplete_index -= 1
        if autocomplete_index < 0:
            autocomplete_index = autocomplete_listbox.size() - 1
        autocomplete_listbox.select_clear(0, "end")
        autocomplete_listbox.select_set(autocomplete_index)
        autocomplete_listbox.activate(autocomplete_index)

    elif event.keysym == "Return":
        if autocomplete_index != -1 and autocomplete_matches:
            selected = autocomplete_matches[autocomplete_index]
            update_search_entry(selected)

def select_autocomplete_from_click(event):
    global autocomplete_listbox
    if autocomplete_listbox:
        index = autocomplete_listbox.curselection()
        if index:
            selected = autocomplete_listbox.get(index)
            update_search_entry(selected)

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
search_entry.bind("<KeyRelease>", show_autocomplete)
search_entry.bind("<Down>", handle_keypress)
search_entry.bind("<Up>", handle_keypress)
search_entry.bind("<Return>", handle_keypress)

search_icon = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="#f2e6f7", bd=0, relief="flat", activebackground="#e0d5f0", cursor="hand2",command=handle_search)
search_icon.pack(side="left", padx=(5, 10))

brand_label = tk.Label(header_frame, text="DATEWAY", font=("Arial", 14, "bold"), bg="white")
brand_label.pack(side="right", padx=20)

#--------- header end ---------

#--------- side start ---------

gif_path = "kakao2.gif"

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

#--------- side end ---------

#--------- list start ---------

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(list_frame, bg="#ffffff", yscrollcommand=scrollbar.set, width=960, height=340)
canvas.pack(side="left", fill="both", expand=True)

scrollbar.config(command=canvas.yview)

places_frame = tk.Frame(canvas, bg="#ffffff", width=960, height=340, pady=40)
canvas.create_window((0, 0), window=places_frame, anchor="nw")

# 카드 클릭시 역 가져오기
def get_courses(station):
    global course, start
    print(f"선택된 역: {station}")

    if station in course:
        if station == course[0] and start is not None:
            return
        course.remove(station)
        print(f"중복 선택 → '{station}' 삭제됨")
    else:
        course.append(station)

    route_repeat(course)
    print(f"[현재 경로] {course}")
    print('')

# 장소카드 클릭이벤트 함수
def click_place(station, title): 
    get_courses(station)

for i, place in enumerate(places):
    if i % 3 == 0:
        wrap = tk.Frame(places_frame, bg="#ffffff")
        wrap.pack(padx=4, pady=10)

    # 장소 카드 영역 생성
    place_card = tk.Frame(wrap, width=300, height=100, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1, cursor="hand2")
    place_card.pack_propagate(0)  # pack_propagate(0) 자동으로 사이즈 조절되는 기능 끄기
    place_card.pack(side="left", fill="y", padx=10)

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