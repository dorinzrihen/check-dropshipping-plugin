import PasteImageArea from "../components/PasteImageArea.tsx";

function Popup() {
  return (
    <div className="flex flex-col">
      <h2>Please drag a photo to this box</h2>
      <PasteImageArea/>
    </div>
  );
}

export default Popup;