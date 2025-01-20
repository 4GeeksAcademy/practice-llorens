import React from "react";

export const SideButtons_left = ({ position }) => (
    <div className={`position-absolute ${position}-0 top-50 translate-middle-y`} style={{ width: '150px', transform: 'translateY(-50%)' }}>
      <ul className="list-unstyled">
        <li><button className="btn btn-secondary w-100 mb-2">Crear una cuenta</button></li>
        <li><button className="btn btn-secondary w-100">Mi cuenta</button></li>
      </ul>
    </div>
  );