import React from 'react';
import logoImage from '../assets/logo.png';

const LogoCopaMundial = ({ size = 80, onClick }) => {
  return (
    <img 
      src={logoImage} 
      alt="Copa Mundial" 
      className="logo-clickable"
      style={{
        width: size,
        height: size,
        objectFit: 'contain',
        cursor: 'pointer'
      }}
      onClick={onClick}
    />
  );
};

export default LogoCopaMundial;
