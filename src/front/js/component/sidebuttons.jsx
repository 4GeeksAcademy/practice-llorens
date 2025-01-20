import React from "react";

export const SideButtons = ({ position }) => (
    <div className={`position-absolute ${position}-0 top-50 translate-middle-y`} style={{ width: '150px', transform: 'translateY(-50%)' }}>
      <ul className="list-unstyled">
        <li><button className="btn btn-secondary w-100 mb-2">Cinemáticas</button></li>
        <li><button className="btn btn-secondary w-100 mb-2">Créditos</button></li>
        <li><button className="btn btn-secondary w-100 mb-2">Política de privacidad</button></li>
        <li><button className="btn btn-secondary w-100 mb-2">Política de cookies</button></li>
      </ul>
    </div>
  );