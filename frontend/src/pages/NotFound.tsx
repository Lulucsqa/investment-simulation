import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
    document.title = "404 - Página não encontrada";
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute('content', '404 página não encontrada - Simulações de investimentos');
  }, [location.pathname]);

  return (
    <main className="min-h-screen flex items-center justify-center bg-background">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-4">404</h1>
        <p className="text-xl text-muted-foreground mb-4">Ops! Página não encontrada</p>
        <Link to="/" className="text-primary hover:opacity-90 underline">
          Voltar ao início
        </Link>
      </section>
    </main>
  );
};

export default NotFound;
