import tkinter as tk
import PIL.ImageOps, PIL.Image, PIL.ImageTk
import imageio
import pandas as pd, os

class App:
    def __init__(self, window, window_title, df_summ_annotated):
        #init
        self.roi_idx = 0
        self.slide_idx = 0        
        self.df_summ_annotated = pd.read_csv(file_name)
        self.image_size = 400

        
        #main windows
        self.window = window
        self.window.title(window_title)
        self.window.geometry("800x600")
        
        
        # present image 
        self.lbl_img_idx = tk.Label(self.window)        
        self.lbl_img_idx.pack()
        self.lbl_img_idx.place(relx = 0.38, rely = 0.02)
                
        self.canvas = tk.Canvas(window, width = self.image_size, height = self.image_size)
        self.canvas.pack()
        self.canvas.place(relx = 0.35, rely = 0.05)
        
        
        self.present_image()
        
        
        #prev and next image buttons
        self.btn_next_image=tk.Button(window, text="Next image", width=10, command=self.next_image)
        self.btn_next_image.pack(anchor=tk.CENTER, expand=False)
        self.btn_next_image.place(relx=0.22, rely=0.2)
        
        self.btn_prev_image=tk.Button(window, text="Previous image", width=12, command=self.prev_image)
        self.btn_prev_image.pack(anchor=tk.CENTER, expand=False)
        self.btn_prev_image.place(relx=0.1, rely=0.2)        
        
        
        #prev and next slide buttons
        self.btn_next_slide=tk.Button(window, text="Next slide", width=10, command=self.next_slide)
        self.btn_next_slide.pack(anchor=tk.CENTER, expand=False)
        self.btn_next_slide.place(relx=0.22, rely=0.25)
        
        self.btn_prev_slide=tk.Button(window, text="Previous slide", width=12, command=self.prev_slide)
        self.btn_prev_slide.pack(anchor=tk.CENTER, expand=False)
        self.btn_prev_slide.place(relx=0.1, rely=0.25)        
        
        
        # select pathology
        self.lbl_path = tk.Label(window, text="Select pathology")
        self.lbl_path.pack()
        self.lbl_path.place(relx=0.1, rely=0.37)
                
        self.v = tk.StringVar()
        self.rbtn_path1 = tk.Radiobutton(window, text="Not selected", variable=self.v, value="Not selected", command=self.rbtn_path_pressed)        
        self.rbtn_path1.select()
        self.rbtn_path1.pack()
        self.rbtn_path1.place(relx=0.1, rely=0.4)
        self.rbtn_path2 = tk.Radiobutton(window, text="Benign", variable=self.v, value="Benign", command=self.rbtn_path_pressed)                
        self.rbtn_path2.pack()
        self.rbtn_path2.place(relx=0.1, rely=0.43)
        self.rbtn_path3 = tk.Radiobutton(window, text="Equivocal", variable=self.v, value="Equivocal", command=self.rbtn_path_pressed)        
        self.rbtn_path3.pack()
        self.rbtn_path3.place(relx=0.1, rely=0.46)
        self.rbtn_path4 = tk.Radiobutton(window, text="Malignant", variable=self.v, value="Malignant", command=self.rbtn_path_pressed)                
        self.rbtn_path4.pack()
        self.rbtn_path4.place(relx=0.1, rely=0.49)
        
        self.window.mainloop()
        

    def present_image(self):
        self.slide_name = self.df_summ_annotated.slide_name.iloc[self.slide_idx]
        self.lbl_img_idx.config(text="Slide index: " + str(self.slide_idx)+ \
                                     ", Image index: " + str(self.roi_idx)+ \
                                     ", Assigned Pathology: " + str(self.df_summ_annotated.roi_path.iloc[self.slide_idx]))        
        self.cv_img = imageio.imread(os.path.join('summarization_images',self.slide_name,str(self.roi_idx)+'.png'))            
#         self.cv_img = self.cv_img[...,[2,1,0]] #bgr2rgb
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.ImageOps.fit(PIL.Image.fromarray(self.cv_img), (self.image_size, self.image_size)))        
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
#         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))        
#         self.imageLabel = tk.Label(self.window, image=self.photo)
#         self.imageLabel.pack()
#         self.imageLabel.place(relx = 0.35, rely = 0.05)
        
        
    def next_image(self):
        self.roi_idx = (self.roi_idx + 1) % 20
        self.present_image()
        
    def prev_image(self):        
        self.roi_idx = (self.roi_idx - 1) % 20
        self.present_image()
    
    
    def next_slide(self):
        self.slide_idx = min(self.slide_idx + 1, len(self.df_summ_annotated))
        self.roi_idx = 0
        self.present_image()
        self.rbtn_path1.select()
        
    def prev_slide(self):
        self.slide_idx = max(self.slide_idx -1, 0)
        self.roi_idx = 0
        self.present_image()   
        self.rbtn_path1.select()
        
    def rbtn_path_pressed(self):        
        self.df_summ_annotated.loc[self.slide_idx, 'roi_path'] = self.v.get()
        self.present_image()
        self.df_summ_annotated.to_csv(file_name, index=False)

file_name = 'df_summ_annoted_prostate_feat_NoisyOr_0_tmp.csv'

App(tk.Tk(), "Prostate Summarization",file_name)