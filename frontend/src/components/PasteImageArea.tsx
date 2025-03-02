import React, { useRef, useState } from 'react';

const PasteImageArea: React.FC = () => {
  const pasteAreaRef = useRef<HTMLDivElement>(null);
  const [imageSrc, setImageSrc] = useState<string>('');
  const [imageFile, setImageFile] = useState<File | null>(null);

  const handleImage = (e: React.ClipboardEvent<HTMLDivElement> | React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    let file: File | null = null;

    if ('clipboardData' in e) {
      // Handle Paste
      const clipboardData = e.clipboardData;
      for (let i = 0; i < clipboardData.items.length; i++) {
        const item = clipboardData.items[i];
        if (item.type.startsWith('image/')) {
          file = item.getAsFile();
          break;
        }
      }
    } else if ('dataTransfer' in e) {
      // Handle Drag & Drop
      if (e.dataTransfer.files.length > 0 && e.dataTransfer.files[0].type.startsWith('image/')) {
        file = e.dataTransfer.files[0];
      }
    }

    if (file) {
      resizeImage(file); // Resize before setting state
    }
  };

  // Resize image before uploading
  const resizeImage = (file: File) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (event) => {
      if (event.target?.result) {
        const img = new Image();
        img.src = event.target.result as string;
        img.onload = () => {
          const maxWidth = 800;
          const maxHeight = 800;
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > maxWidth) {
              height *= maxWidth / width;
              width = maxWidth;
            }
          } else {
            if (height > maxHeight) {
              width *= maxHeight / height;
              height = maxHeight;
            }
          }

          // Create a canvas and resize the image
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d')!;
          canvas.width = width;
          canvas.height = height;
          ctx.drawImage(img, 0, 0, width, height);

          // Convert canvas to Blob
          canvas.toBlob((blob) => {
            if (blob) {
              const resizedFile = new File([blob], "resized_image.png", { type: "image/png" });
              setImageFile(resizedFile); // Store resized file
              setImageSrc(URL.createObjectURL(resizedFile)); // Show preview
            }
          }, 'image/png', 0.7);
        };
      }
    };
  };

  const uploadImage = async () => {
    if (!imageFile) return;

    const formData = new FormData();
    formData.append("image", imageFile);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
      });

      const result = await response.json();
      console.log("Server Response:", result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      {!imageSrc ? (
        <div
          ref={pasteAreaRef}
          onPaste={handleImage}
          onDrop={handleImage}
          onDragOver={(e) => e.preventDefault()}
          style={{
            border: '2px dashed #ccc',
            padding: '10px',
            width: '300px',
            height: '150px',
            marginBottom: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            color: '#888',
          }}
        >
          Paste or drag an image here...
        </div>
      ) : (
        <img
          src={imageSrc}
          alt="Pasted Preview"
          style={{
            maxWidth: '100%',
            border: '1px solid #eee',
            padding: '5px',
            width: '300px',
            height: '150px',
          }}
        />
      )}
      <button onClick={uploadImage} disabled={!imageFile}>
        Upload
      </button>
    </div>
  );
};

export default PasteImageArea;
