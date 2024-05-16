# შემოგვაქვს სასურველი ბიბლიოთეკები
import requests
import json
import sqlite3

# აპი-ს ლინკი
LINK = "https://api.thecatapi.com/v1/images/search"

# შეიქმნა კატის კლასი, სადაც დავამატეთ ფუნქცია, რომ ის ბაზაში დაემატოს
class Cat:
    # აღვწერეთ კატა
    def __init__(self,id,image_link,width,height):
        self.id = id
        self.image_link = image_link
        self.width = width
        self.height = height

# ამ მეთოდის საშუალებით ემატება ჩვენს დატაბაზაში
    def add_to_base(self):
        curs.execute('''INSERT INTO cats (site_id,image_link,width,height) VALUES (?,?,?,?)''',
                     (self.id,self.image_link,self.width,self.height))
        conn.commit()

# შევქმენით ფუნქცია, რომელიც http მოთხოვნას აგზავნის მითითებულ API-ზე, შემდეგ დაბრუნებული ინფორმაცია მუშავდება, თუ
# სტატუს კოდი დაგვიბრუნდა 200, რაც ნიშნავს, რომ კავშირი წარმატებით დამყარდა, შემდგომ ინფორმაცია ინახება ბაზაში

def generate_cat():
    cats = []
    resp = requests.get(f"{LINK}?limit=10")
    if resp.status_code == 200:
        resp = json.loads(resp.text)
        for data in resp:
            cat = Cat(data['id'], data['url'],data['width'],data['height'])
            cats.append(cat)
        for cat in cats:
            cat.add_to_base()
    else:
        print(f"სერვერთან კავშირი ვერ მოხერხდა\nსტატუსის კოდი: {resp.status_code}\nიხილეთ კოდები შემდეგ ლინკზე: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status")

# შეიქმნა ფუნქცია, რომლის მეშვეობითან ბაზიდან ვიღებთ კატების ფოტოების ლინკებს, ხოლო შემდეგ ვპრინტავთ მათ
def read_cats():
    cat_images = curs.execute('''SELECT image_link FROM cats''').fetchall()

    for cat_image in cat_images:
        print(cat_image)

# შეიქმნა ფუნქცია, რომლის გამოძახების შემთხვევაში ბაზა გასუფთავდება.

def delete_cats():
    curs.execute('''DELETE FROM cats WHERE id > 0''')
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('imagesofcats.db')
    curs = conn.cursor()

# იქმნება მონაცემთა ბაზა, რომელშიც შეინახება კატის ფოტოები, ფოტოს ზომა და მისი აიდი

    curs.execute('''CREATE TABLE IF NOT EXISTS cats 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT,
    image_link TEXT,
    width TEXT,
    height TEXT)''')


    generate_cat()

    read_cats()

    #delete_cats()

    conn.close()

# ლ.ვარსიმაშვილი :)

