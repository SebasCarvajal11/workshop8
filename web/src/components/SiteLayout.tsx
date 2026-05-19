import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useCart } from "../cart/CartContext";
import { MastheadDate } from "./MastheadDate";

const nav = [
  { to: "/", label: "Portada", end: true },
  { to: "/entrevista", label: "Entrevista", end: false },
  { to: "/canasta", label: "Canasta", end: false },
] as const;

export function SiteLayout() {
  const { count } = useCart();
  const { pathname } = useLocation();
  const isHome = pathname === "/";

  return (
    <div
      className={`app-shell newspaper${isHome ? " app-shell--viewport" : " app-shell--scroll"}`}
    >
      <header className="site-header masthead masthead--compact">
        <div className="masthead-row">
          <MastheadDate />
          <div className="brand-block">
            <NavLink to="/" className="masthead-title">
              <span className="brand-line">El Mercantil</span>
            </NavLink>
            <span className="brand-tagline">
              Bolsa de precios dinámicos · motor CLIPS
            </span>
          </div>
        </div>
        <nav className="masthead-nav" aria-label="Secciones">
          {nav.map(({ to, label, end }) => (
            <span key={to} className="nav-item-wrap">
              <NavLink
                to={to}
                end={end}
                className={({ isActive }) =>
                  isActive ? "nav-link nav-link--active" : "nav-link"
                }
              >
                {label}
                {to === "/canasta" && count > 0 ? (
                  <span className="badge badge--inline">{count}</span>
                ) : null}
              </NavLink>
            </span>
          ))}
        </nav>
        <hr className="rule-double rule-double--compact" />
        <hr className="rule-thin rule-thin--compact" />
      </header>
      <main
        className={`site-main${isHome ? " site-main--viewport" : " site-main--scroll"}`}
        id="contenido-principal"
      >
        <Outlet />
      </main>
      <footer className="site-footer site-footer--compact">
        <p>
          Workshop 5 — Sistemas basados en reglas · 11 reglas · proposiciones
          DA–GE
        </p>
      </footer>
    </div>
  );
}
