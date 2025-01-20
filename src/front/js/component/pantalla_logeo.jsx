import React, { useState } from "react";
import { MainLogo } from "./logo.jsx";
import { SideButtons } from "./sidebuttons.jsx";
import { LoginForm } from "./login_form.jsx";
import { FooterLogo } from "./footer_logo.jsx";
import background from "../../img/CQx.gif";
import { SideButtons_left } from "./sidebuttons_left.jsx";
import { RegisterForm } from "./register_form.jsx";

const LoginScreen = () => {
    const [action, setAction] = useState('login');

    return (
        <div
            className="position-relative vh-100 bg-dark"
            style={{
                backgroundImage: `url(${background})`,
                backgroundSize: "cover",
                backgroundPosition: "center",
            }}
        >
            <MainLogo />
            <div
                className="d-flex flex-column align-items-center justify-content-center"
                style={{ height: "calc(100% - 200px)" }}
            >
                <div className="d-flex align-items-center justify-content-center">
                    <button type="submit" className="btn btn-danger me-3" onClick={() => setAction('login')}>
                        Iniciar Sesión
                    </button>
                    <button type="submit" className="btn btn-danger" onClick={() => setAction('register')}>
                        Registrarse
                    </button>
                </div>
                {action === 'login' ? <LoginForm /> : <RegisterForm />}
                <FooterLogo />
            </div>
            <div className="position-relative w-60" style={{ bottom: 0 }}>
                <SideButtons_left position="start" />
                <SideButtons position="end" />
            </div>
        </div>
    );
};

export default LoginScreen;
