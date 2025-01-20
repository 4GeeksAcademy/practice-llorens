import React from "react";
import logo from "../../img/logo.png"

export const MainLogo = () => (
    <div className="text-start py-3">
      <img src={logo} alt="Main Logo" className="img-fluid" style={{ maxWidth: '300px' }} />
    </div>
  );