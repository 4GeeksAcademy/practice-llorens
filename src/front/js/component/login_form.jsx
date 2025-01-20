import React from "react";

export const LoginForm = () => (
    <div className="d-flex flex-column align-items-center py-4">
      <form className="bg-transparent p-4 border border-light rounded" style={{ width: '300px' }}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label text-white">Nombre de Usuario</label>
          <input type="text" className="form-control" id="username" />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label text-white">Contraseña</label>
          <input type="password" className="form-control" id="password" />
        </div>
        <div className="mb-3 form-check">
          <input type="checkbox" className="form-check-input" id="rememberMe" />
          <label className="form-check-label text-white" htmlFor="rememberMe">¿Recordar contraseña?</label>
        </div>
        <button type="submit" className="btn btn-danger w-100">Login</button>
      </form>
    </div>
  );