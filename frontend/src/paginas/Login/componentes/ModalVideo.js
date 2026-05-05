import React, { useEffect, useRef } from 'react';

const ModalVideo = ({ isOpen, onClose, videoId }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    const modal = modalRef.current;
    
    if (!modal) return;

    if (isOpen) {
      // Forzar reflow y añadir clase
      void modal.offsetHeight; // Force reflow
      modal.classList.add('active');
    } else {
      modal.classList.remove('active');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div ref={modalRef} className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <div className="video-container">
          <iframe
            width="100%"
            height="100%"
            src={`https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&modestbranding=1&rel=0`}
            title="Video del Mundial"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"
            allowFullScreen
          />
        </div>
      </div>
    </div>
  );
};

export default ModalVideo;
