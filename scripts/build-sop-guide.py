from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "SOP 工具組_使用教學.pdf"

W, H = A4
RED = HexColor("#C8102E")
RED_LIGHT = HexColor("#FBEAEC")
INK = HexColor("#17202A")
MUTED = HexColor("#637083")
LINE = HexColor("#D8DEE7")
PANEL = HexColor("#F6F8FB")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#18864B")
AMBER = HexColor("#B96A08")

pdfmetrics.registerFont(TTFont("NotoTC", r"C:\Windows\Fonts\msjh.ttc"))
pdfmetrics.registerFont(TTFont("NotoTC-Bold", r"C:\Windows\Fonts\msjhbd.ttc"))


def para(c, text, x, y_top, width, size=11, leading=17, color=INK,
         font="NotoTC", align=0):
    style = ParagraphStyle(
        "p",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align,
        spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, ph = p.wrap(width, H)
    p.drawOn(c, x, y_top - ph)
    return ph


def round_rect(c, x, y, width, height, fill=PANEL, stroke=LINE, radius=4 * mm):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, height, radius, fill=1, stroke=1)


def page_header(c, kicker, title, intro, page):
    c.setFillColor(RED)
    c.roundRect(18 * mm, H - 25 * mm, 35 * mm, 8 * mm, 4 * mm, fill=1, stroke=0)
    para(c, kicker, 18 * mm, H - 19.6 * mm, 35 * mm, 8.5, 10,
         WHITE, "NotoTC-Bold", TA_CENTER)
    para(c, title, 18 * mm, H - 35 * mm, 174 * mm, 25, 31,
         INK, "NotoTC-Bold")
    para(c, intro, 18 * mm, H - 52 * mm, 174 * mm, 10.5, 16, MUTED)
    c.setStrokeColor(LINE)
    c.line(18 * mm, H - 61 * mm, 192 * mm, H - 61 * mm)
    c.setFont("NotoTC", 8)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, 10 * mm, "SOP 工具組｜內部使用教學")
    c.drawRightString(192 * mm, 10 * mm, f"{page} / 4")


def label(c, text, x, y, width=25 * mm, color=RED):
    c.setFillColor(color)
    c.roundRect(x, y, width, 7 * mm, 3.5 * mm, fill=1, stroke=0)
    para(c, text, x, y + 5.4 * mm, width, 8.4, 10, WHITE,
         "NotoTC-Bold", TA_CENTER)


def numbered_card(c, number, title, body, x, y, width, height, accent=RED):
    round_rect(c, x, y, width, height, WHITE, LINE)
    c.setFillColor(accent)
    c.circle(x + 11 * mm, y + height - 12 * mm, 5.4 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("NotoTC-Bold", 11)
    c.drawCentredString(x + 11 * mm, y + height - 15.5 * mm, str(number))
    para(c, title, x + 21 * mm, y + height - 8 * mm, width - 27 * mm,
         12.5, 16, INK, "NotoTC-Bold")
    para(c, body, x + 8 * mm, y + height - 27 * mm, width - 16 * mm,
         9.5, 14, MUTED)


def key(c, text, x, y, width=None):
    width = width or max(12 * mm, (len(text) * 3.2 + 7) * mm)
    c.setFillColor(WHITE)
    c.setStrokeColor(HexColor("#B8C0CC"))
    c.roundRect(x, y, width, 7 * mm, 1.8 * mm, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont("NotoTC-Bold", 8.5)
    c.drawCentredString(x + width / 2, y + 2.1 * mm, text)
    return width


def delivery_card(c, number, title, body, x, y, width, accent):
    height = 32 * mm
    round_rect(c, x, y, width, height, WHITE, LINE)
    c.setFillColor(accent)
    c.circle(x + 10 * mm, y + height - 11 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("NotoTC-Bold", 10)
    c.drawCentredString(x + 10 * mm, y + height - 14 * mm, str(number))
    para(c, title, x + 19 * mm, y + height - 7 * mm, width - 24 * mm,
         10.5, 13, INK, "NotoTC-Bold")
    para(c, body, x + 8 * mm, y + height - 19 * mm, width - 16 * mm,
         7.8, 10.5, MUTED)


def page_one(c):
    page_header(
        c,
        "快速開始",
        "把操作過程，整理成人人看得懂的 SOP",
        "不需要安裝軟體。用 Chrome 或 Edge 開啟工具，加入畫面、標註重點、記錄工時，再匯出交件。",
        1,
    )
    y = H - 106 * mm
    card_w = 83 * mm
    card_h = 47 * mm
    numbered_card(c, 1, "加入畫面", "貼上截圖、拖入多張圖片，或匯入螢幕錄影後按 M 擷取關鍵畫面。", 18 * mm, y, card_w, card_h)
    numbered_card(c, 2, "標註重點", "預設就是常用的矩形工具。框選、箭頭、標號、貼圖完成後仍可再次選取與調整。", 109 * mm, y, card_w, card_h)
    y2 = y - 56 * mm
    numbered_card(c, 3, "記錄工時", "新增工時卡片時可直接插在指定位置；費率以每分鐘 NT$5 計算。", 18 * mm, y2, card_w, card_h)
    numbered_card(c, 4, "匯出交件", "下載可再編輯的 .sop.html，或輸出書面 HTML／PDF。管理者也可直接取代既有流程。", 109 * mm, y2, card_w, card_h)
    round_rect(c, 18 * mm, 24 * mm, 174 * mm, 24 * mm, RED_LIGHT, RED_LIGHT)
    para(c, "記得保留 <b>.sop.html</b>", 24 * mm, 43 * mm, 48 * mm, 11, 15, RED, "NotoTC-Bold")
    para(c, "這是可再次開啟、繼續編輯的原始檔；PDF 適合閱讀與列印，但不能回到工具中接著改。", 72 * mm, 43 * mm, 112 * mm, 9.2, 14, INK)


def page_two(c):
    page_header(
        c,
        "製圖頁",
        "標註可以重選、移動，也能放大縮小",
        "先用滑鼠選取物件，再拖曳本體移動位置；拖曳外框控制點調整大小。完成後不必刪掉重畫。",
        2,
    )
    left = 18 * mm
    top_y = H - 72 * mm
    round_rect(c, left, top_y - 77 * mm, 113 * mm, 77 * mm, WHITE, LINE)
    label(c, "編輯方式", left + 8 * mm, top_y - 14 * mm, 25 * mm)
    para(c, "1　點一下既有的矩形、箭頭、標號或貼圖", left + 8 * mm, top_y - 25 * mm, 97 * mm, 10.2, 15, INK, "NotoTC-Bold")
    para(c, "2　拖曳物件本體，可移動到新的位置", left + 8 * mm, top_y - 40 * mm, 97 * mm, 10.2, 15, INK, "NotoTC-Bold")
    para(c, "3　拖曳外框控制點，可放大也可縮小", left + 8 * mm, top_y - 55 * mm, 97 * mm, 10.2, 15, INK, "NotoTC-Bold")
    para(c, "貼圖不再被舊版最小尺寸卡住；舊檔中尚未調整過的貼圖仍維持原本預設大小。", left + 8 * mm, top_y - 68 * mm, 97 * mm, 8.8, 13, MUTED)

    # A compact visual example of a selected sticker and its resize handle.
    box_x, box_y = 142 * mm, top_y - 62 * mm
    round_rect(c, 136 * mm, top_y - 77 * mm, 56 * mm, 77 * mm, PANEL, LINE)
    para(c, "貼圖縮放示意", 142 * mm, top_y - 10 * mm, 44 * mm, 9.5, 13, MUTED, "NotoTC-Bold", TA_CENTER)
    c.setStrokeColor(RED)
    c.setLineWidth(1.4)
    c.rect(box_x, box_y, 32 * mm, 32 * mm, fill=0, stroke=1)
    c.setFillColor(HexColor("#FFD34D"))
    c.circle(box_x + 16 * mm, box_y + 16 * mm, 9 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.circle(box_x + 13 * mm, box_y + 18 * mm, 1 * mm, fill=1, stroke=0)
    c.circle(box_x + 19 * mm, box_y + 18 * mm, 1 * mm, fill=1, stroke=0)
    c.setStrokeColor(INK)
    c.arc(box_x + 11 * mm, box_y + 10 * mm, box_x + 21 * mm, box_y + 18 * mm, 200, 140)
    c.setFillColor(RED)
    c.rect(box_x + 29.5 * mm, box_y - 2.5 * mm, 5 * mm, 5 * mm, fill=1, stroke=0)
    c.setStrokeColor(RED)
    c.line(box_x + 32 * mm, box_y, box_x + 20 * mm, box_y + 12 * mm)
    para(c, "往內拖，就會縮小", 142 * mm, top_y - 70 * mm, 44 * mm, 8.8, 12, RED, "NotoTC-Bold", TA_CENTER)

    round_rect(c, 18 * mm, 66 * mm, 174 * mm, 56 * mm, PANEL, LINE)
    label(c, "鍵盤操作", 26 * mm, 108 * mm, 25 * mm, INK)
    x = 27 * mm
    y = 91 * mm
    w = key(c, "Esc", x, y, 16 * mm)
    para(c, "取消正在畫的物件／回到選取工具", x + w + 4 * mm, y + 6 * mm, 66 * mm, 9.2, 12, INK)
    x = 108 * mm
    w = key(c, "Ctrl + Z", x, y, 25 * mm)
    para(c, "復原", x + w + 4 * mm, y + 6 * mm, 28 * mm, 9.2, 12, INK)
    x = 27 * mm
    y = 76 * mm
    w = key(c, "Ctrl + C / V", x, y, 32 * mm)
    para(c, "複製／貼上選取的標註", x + w + 4 * mm, y + 6 * mm, 55 * mm, 9.2, 12, INK)
    x = 108 * mm
    w = key(c, "Ctrl + Y", x, y, 25 * mm)
    para(c, "重做", x + w + 4 * mm, y + 6 * mm, 28 * mm, 9.2, 12, INK)
    para(c, "Esc 不會再把整個編輯器關掉。要離開編輯器，請使用畫面上的完成／關閉按鈕。", 26 * mm, 69 * mm, 156 * mm, 8.8, 12, MUTED)

    round_rect(c, 18 * mm, 24 * mm, 174 * mm, 29 * mm, WHITE, LINE)
    label(c, "小提醒", 26 * mm, 42 * mm, 21 * mm, GREEN)
    para(c, "找不到選取狀態時，先按 Esc 回到選取工具；再點一下要調整的物件。", 52 * mm, 47 * mm, 130 * mm, 9.5, 14, INK, "NotoTC-Bold")


def page_three(c):
    page_header(
        c,
        "工時與輸出",
        "卡片插在對的位置，再選擇交付格式",
        "工時卡片的新增方式與製圖卡片一致，不必再從最下面慢慢往上拖；金額統一以每分鐘 NT$5 計算。",
        3,
    )
    round_rect(c, 18 * mm, H - 150 * mm, 174 * mm, 77 * mm, WHITE, LINE)
    label(c, "工時卡片", 26 * mm, H - 91 * mm, 25 * mm)
    para(c, "把滑鼠移到兩張卡片之間，點出現的 ＋", 26 * mm, H - 104 * mm, 110 * mm, 12, 17, INK, "NotoTC-Bold")
    para(c, "新卡片會直接插入那個位置。內容可再次編輯，排序也可用拖曳調整。", 26 * mm, H - 119 * mm, 102 * mm, 9.5, 14, MUTED)
    # Three cards and insertion marker.
    y = H - 143 * mm
    for i, text in enumerate(("準備", "操作", "確認")):
        x = 136 * mm + (i % 2) * 24 * mm
        yy = y + (1 - i // 2) * 21 * mm
        c.setFillColor(PANEL)
        c.setStrokeColor(LINE)
        c.roundRect(x, yy, 20 * mm, 15 * mm, 2 * mm, fill=1, stroke=1)
        para(c, text, x, yy + 10.5 * mm, 20 * mm, 8.5, 10, INK, "NotoTC-Bold", TA_CENTER)
    c.setStrokeColor(RED)
    c.setLineWidth(1.6)
    c.line(158 * mm, y + 20 * mm, 158 * mm, y + 38 * mm)
    c.setFillColor(RED)
    c.circle(158 * mm, y + 29 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("NotoTC-Bold", 12)
    c.drawCentredString(158 * mm, y + 25.5 * mm, "+")

    round_rect(c, 18 * mm, 71 * mm, 174 * mm, 61 * mm, PANEL, LINE)
    label(c, "三種交付", 26 * mm, 117 * mm, 25 * mm, INK)
    delivery_card(c, 1, ".sop.html", "可再匯入工具修改；交接與封存時保留。", 25 * mm, 76 * mm, 50 * mm, GREEN)
    delivery_card(c, 2, "書面 HTML", "瀏覽器直接閱讀；一步一圖，方便寄送。", 80 * mm, 76 * mm, 50 * mm, AMBER)
    delivery_card(c, 3, "PDF", "適合定稿列印；由書面版另存 PDF。", 135 * mm, 76 * mm, 50 * mm, RED)

    round_rect(c, 18 * mm, 24 * mm, 174 * mm, 34 * mm, RED_LIGHT, RED_LIGHT)
    para(c, "費率已更新", 26 * mm, 49 * mm, 37 * mm, 10.5, 14, RED, "NotoTC-Bold")
    para(c, "工時費用＝總分鐘數 × NT$5", 64 * mm, 50 * mm, 70 * mm, 12, 16, INK, "NotoTC-Bold")
    para(c, "舊檔重新開啟後，會依新版費率顯示與計算。", 64 * mm, 37 * mm, 116 * mm, 8.8, 12, MUTED)


def page_four(c):
    page_header(
        c,
        "管理者交件",
        "檔名不同，也能指定一筆既有流程直接取代",
        "管理者專用匯入後台以流程清單為準，不用猜檔名。從連結總表開啟後，選擇要取代的流程再上傳。",
        4,
    )
    y = H - 107 * mm
    card_w = 52 * mm
    card_h = 42 * mm
    numbered_card(c, 1, "選檔", "選擇本機的 .sop.html。檔名可以和線上流程不同。", 18 * mm, y, card_w, card_h)
    numbered_card(c, 2, "指定流程", "從既有流程清單選一筆；畫面會清楚顯示將被取代的對象。", 79 * mm, y, card_w, card_h)
    numbered_card(c, 3, "確認取代", "核對流程名稱後執行。完成時會回報更新結果。", 140 * mm, y, card_w, card_h)

    round_rect(c, 18 * mm, 86 * mm, 174 * mm, 57 * mm, WHITE, LINE)
    label(c, "取代規則", 26 * mm, 129 * mm, 25 * mm, INK)
    para(c, "會更新", 27 * mm, 116 * mm, 28 * mm, 10, 14, GREEN, "NotoTC-Bold")
    para(c, "流程內容、步驟圖片、標註與工時資料", 56 * mm, 116 * mm, 119 * mm, 9.5, 14, INK)
    c.setStrokeColor(LINE)
    c.line(27 * mm, 109 * mm, 182 * mm, 109 * mm)
    para(c, "會保留", 27 * mm, 104 * mm, 28 * mm, 10, 14, AMBER, "NotoTC-Bold")
    para(c, "線上既有流程的管理欄位與識別資料", 56 * mm, 104 * mm, 119 * mm, 9.5, 14, INK)
    c.setStrokeColor(LINE)
    c.line(27 * mm, 97 * mm, 182 * mm, 97 * mm)
    para(c, "不需要", 27 * mm, 92 * mm, 28 * mm, 10, 14, RED, "NotoTC-Bold")
    para(c, "讓上傳檔名和既有流程名稱完全一樣", 56 * mm, 92 * mm, 119 * mm, 9.5, 14, INK)

    round_rect(c, 18 * mm, 43 * mm, 174 * mm, 31 * mm, PANEL, LINE)
    label(c, "從哪裡開", 26 * mm, 61 * mm, 28 * mm, RED)
    para(c, "連結總表 →「SOP 匯入後台（限管理者）」", 59 * mm, 66 * mm, 123 * mm, 11, 15, INK, "NotoTC-Bold")
    para(c, "一般使用者不會看到此入口；請以 SHAN 管理帳號操作。", 59 * mm, 53 * mm, 123 * mm, 8.8, 12, MUTED)

    round_rect(c, 18 * mm, 20 * mm, 174 * mm, 16 * mm, RED_LIGHT, RED_LIGHT)
    para(c, "取代會直接更新線上既有流程。送出前請再看一次選到的流程名稱。", 25 * mm, 32 * mm, 160 * mm, 9.2, 13, RED, "NotoTC-Bold", TA_CENTER)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("SOP 工具組｜使用教學")
    c.setAuthor("REXON")
    for draw in (page_one, page_two, page_three, page_four):
        draw(c)
        c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
