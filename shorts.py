import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

def create_slideshow(image_folder, audio_file, output_file, duration_per_image, end_time):
    # Lista de imágenes en el directorio
    image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        messagebox.showerror(translations[lang]['error'], translations[lang]['no_images'])
        return

    # Ordenar las imágenes por nombre
    image_files.sort()

    # Crear clips de imágenes con una duración especificada
    clips = [ImageClip(img).set_duration(duration_per_image).set_fps(24) for img in image_files]  # Aquí se especifica el fps

    # Añadir efecto de transición de desvanecimiento entre los clips
    clips = [clip.crossfadein(1) for clip in clips]

    # Repetir los clips de imágenes para que coincidan con la duración total deseada
    total_clips_duration = len(clips) * duration_per_image
    num_repeats = (end_time // total_clips_duration) + 1
    repeated_clips = clips * num_repeats
    image_sequence = concatenate_videoclips(repeated_clips[:int(end_time / duration_per_image)], method="compose")

    # Cargar el audio y obtener su duración
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration

    # Ajustar la duración del video y del audio al tiempo final especificado
    video_duration = min(audio_duration, end_time)
    image_sequence = image_sequence.subclip(0, video_duration)
    audio = audio.subclip(0, video_duration)

    # Añadir audio al video
    video = image_sequence.set_audio(audio)

    # Exportar el video
    video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24)  # Aquí también se especifica el fps

    # Mostrar mensaje de finalización
    messagebox.showinfo(translations[lang]['success'], translations[lang]['video_created'])

def on_closing():
    if messagebox.askokcancel(translations[lang]['exit'], translations[lang]['exit_confirm']):
        root.destroy()

def suggest_output_filename(directory):
    base_name = "output"
    extension = ".mp4"
    i = 1
    while os.path.exists(os.path.join(directory, f"{base_name}{i}{extension}")):
        i += 1
    return os.path.join(directory, f"{base_name}{i}{extension}")

def select_image_folder():
    folder = filedialog.askdirectory(title=translations[lang]['select_image_dir'])
    if folder:
        image_folder_var.set(folder)
        image_files_var.set(", ".join([f for f in os.listdir(folder) if f.endswith(('jpeg', 'jpg', 'png'))]))

def select_audio_file():
    file = filedialog.askopenfilename(title=translations[lang]['select_audio'], filetypes=[(translations[lang]['audio_files'], "*.mp3 *.wav")])
    if file:
        audio_file_var.set(file)
        audio_files_var.set(os.path.basename(file))

def select_output_folder():
    folder = filedialog.askdirectory(title=translations[lang]['select_output_dir'])
    if folder:
        output_folder_var.set(folder)
        output_file_var.set(suggest_output_filename(folder))

def change_language():
    global lang
    lang = 'en' if lang == 'es' else 'es'
    update_labels()

def show_about():
    messagebox.showinfo("Acerca de", "Esta aplicación fue creada por Enigma.")

def update_labels():
    root.title(translations[lang]['title'])
    img_label.config(text=translations[lang]['image_dir'])
    audio_label.config(text=translations[lang]['audio_file'])
    output_dir_label.config(text=translations[lang]['output_dir'])
    output_file_label.config(text=translations[lang]['output_file'])
    duration_label.config(text=translations[lang]['duration'])
    end_time_label.config(text=translations[lang]['end_time'])
    create_button.config(text=translations[lang]['create_slideshow'])
    change_lang_button.config(text=translations[lang]['change_lang'])
    img_button.config(text=translations[lang]['select'], bg='#FF5733', fg='#FFFFFF')
    audio_button.config(text=translations[lang]['select'], bg='#33FF57', fg='#FFFFFF')
    output_dir_button.config(text=translations[lang]['select'], bg='#3357FF', fg='#FFFFFF')
    about_button.config(text="About", bg='#E74C3C', fg='#FFFFFF')

if __name__ == "__main__":
    root = tk.Tk()
    lang = 'es'  # Default language
    translations = {
        'es': {
            'title': 'Creador de Slideshow',
            'image_dir': 'Directorio de imágenes:',
            'audio_file': 'Archivo de audio:',
            'output_dir': 'Directorio de salida:',
            'output_file': 'Archivo de salida:',
            'duration': 'Duración por imagen (segundos):',
            'end_time': 'Tiempo final del video (segundos):',
            'create_slideshow': 'Crear Slideshow',
            'change_lang': 'Cambiar a Inglés',
            'select': 'Seleccionar',
            'error': 'Error',
            'no_images': 'No se encontraron imágenes en el directorio especificado.',
            'exit': 'Salir',
            'exit_confirm': '¿Quieres salir de la aplicación?',
            'select_image_dir': 'Selecciona el directorio de imágenes',
            'select_audio': 'Selecciona la canción',
            'audio_files': 'Archivos de audio',
            'select_output_dir': 'Selecciona el directorio de salida',
            'success': 'Éxito',
            'video_created': 'El video se ha creado exitosamente.'
        },
        'en': {
            'title': 'Slideshow Creator',
            'image_dir': 'Image Directory:',
            'audio_file': 'Audio File:',
            'output_dir': 'Output Directory:',
            'output_file': 'Output File:',
            'duration': 'Duration per image (seconds):',
            'end_time': 'End time of the video (seconds):',
            'create_slideshow': 'Create Slideshow',
            'change_lang': 'Change to Spanish',
            'select': 'Select',
            'error': 'Error',
            'no_images': 'No images found in the specified directory.',
            'exit': 'Exit',
            'exit_confirm': 'Do you want to exit the application?',
            'select_image_dir': 'Select Image Directory',
            'select_audio': 'Select Audio File',
            'audio_files': 'Audio Files',
            'select_output_dir': 'Select Output Directory',
            'success': 'Success',
            'video_created': 'The video has been created successfully.'
        }
    }

    # Tamaño de la ventana: 80% de 1900x1200
    window_width = int(1900 * 0.8)
    window_height = int(1200 * 0.8)
    root.geometry(f"{window_width}x{window_height}")
    root.configure(background='#ADD8E6')  # Cambiar el fondo a un color más amigable

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Estilo de la interfaz
    style = ttk.Style()
    style.configure('TLabel', font=('Helvetica', 18), padding=10, background='#ADD8E6', foreground='#000000')
    style.configure('TButton', font=('Helvetica', 18), padding=10)
    style.configure('TFrame', background='#ADD8E6')

    main_frame = ttk.Frame(root, padding="20", style='TFrame')
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Variables para almacenar las rutas seleccionadas
    image_folder_var = tk.StringVar(value=os.path.join(current_dir, 'img'))
    audio_file_var = tk.StringVar(value=os.path.join(current_dir, 'audio', 'audio.mp3'))
    output_folder_var = tk.StringVar(value=os.path.join(current_dir, 'output'))
    output_file_var = tk.StringVar(value=suggest_output_filename(os.path.join(current_dir, 'output')))
    duration_var = tk.IntVar(value=5)
    end_time_var = tk.IntVar(value=60)  # Valor predeterminado para la duración del video

    image_files_var = tk.StringVar(value="")
    audio_files_var = tk.StringVar(value="")

    # Elementos de la interfaz
    img_label = ttk.Label(main_frame)
    img_entry = ttk.Entry(main_frame, textvariable=image_folder_var, width=50, font=('Helvetica', 14))
    img_button = tk.Button(main_frame, command=select_image_folder, bg='#FF5733', fg='#FFFFFF')
    img_files_label = ttk.Label(main_frame, textvariable=image_files_var, wraplength=800, background='#ADD8E6', foreground='#000000', font=('Helvetica', 12))

    audio_label = ttk.Label(main_frame)
    audio_entry = ttk.Entry(main_frame, textvariable=audio_file_var, width=50, font=('Helvetica', 14))
    audio_button = tk.Button(main_frame, command=select_audio_file, bg='#33FF57', fg='#FFFFFF')
    audio_files_label = ttk.Label(main_frame, textvariable=audio_files_var, wraplength=800, background='#ADD8E6', foreground='#000000', font=('Helvetica', 12))

    output_dir_label = ttk.Label(main_frame)
    output_dir_entry = ttk.Entry(main_frame, textvariable=output_folder_var, width=50, font=('Helvetica', 14))
    output_dir_button = tk.Button(main_frame, command=select_output_folder, bg='#3357FF', fg='#FFFFFF')

    output_file_label = ttk.Label(main_frame)
    output_file_entry = ttk.Entry(main_frame, textvariable=output_file_var, width=50, font=('Helvetica', 14))

    duration_label = ttk.Label(main_frame)
    duration_entry = ttk.Entry(main_frame, textvariable=duration_var, width=10, font=('Helvetica', 14))

    end_time_label = ttk.Label(main_frame)
    end_time_entry = ttk.Entry(main_frame, textvariable=end_time_var, width=10, font=('Helvetica', 14))

    create_button = tk.Button(main_frame, command=lambda: create_slideshow(image_folder_var.get(), audio_file_var.get(), output_file_var.get(), duration_var.get(), end_time_var.get()), bg='#F1C40F', fg='#FFFFFF')
    change_lang_button = tk.Button(main_frame, command=change_language, bg='#9B59B6', fg='#FFFFFF')
    about_button = tk.Button(main_frame, text="About", command=show_about, bg='#E74C3C', fg='#FFFFFF')

    img_label.grid(row=0, column=0, sticky=tk.W)
    img_entry.grid(row=0, column=1, padx=10)
    img_button.grid(row=0, column=2)
    img_files_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)

    audio_label.grid(row=2, column=0, sticky=tk.W)
    audio_entry.grid(row=2, column=1, padx=10)
    audio_button.grid(row=2, column=2)
    audio_files_label.grid(row=3, column=0, columnspan=3, sticky=tk.W)

    output_dir_label.grid(row=4, column=0, sticky=tk.W)
    output_dir_entry.grid(row=4, column=1, padx=10)
    output_dir_button.grid(row=4, column=2)

    output_file_label.grid(row=5, column=0, sticky=tk.W)
    output_file_entry.grid(row=5, column=1, padx=10)

    duration_label.grid(row=6, column=0, sticky=tk.W)
    duration_entry.grid(row=6, column=1, padx=10)

    end_time_label.grid(row=7, column=0, sticky=tk.W)
    end_time_entry.grid(row=7, column=1, padx=10)

    create_button.grid(row=8, column=0, columnspan=3, pady=20)
    change_lang_button.grid(row=9, column=0, columnspan=3, pady=20)
    about_button.grid(row=10, column=0, columnspan=3, pady=20)

    update_labels()
    root.mainloop()

