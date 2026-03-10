import React, { useState, useEffect, useRef } from 'react';
import { 
  Code2, 
  Layers, 
  Smartphone, 
  Zap, 
  ArrowRight, 
  Github
} from 'lucide-react';

// --- Utility: Scroll Reveal Component ---
const FadeIn = ({ children, delay = 0, direction = 'up', className = '' }) => {
  const [isVisible, setIsVisible] = useState(false);
  const domRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });

    const currentRef = domRef.current;
    if (currentRef) observer.observe(currentRef);
    return () => { if (currentRef) observer.unobserve(currentRef); };
  }, []);

  const getTransform = () => {
    if (isVisible) return 'translate-y-0 translate-x-0 scale-100';
    switch (direction) {
      case 'up': return 'translate-y-12 scale-95';
      case 'down': return '-translate-y-12 scale-95';
      case 'left': return 'translate-x-12 scale-95';
      case 'right': return '-translate-x-12 scale-95';
      default: return 'translate-y-12 scale-95';
    }
  };

  return (
    <div
      ref={domRef}
      className={`transition-all duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)] ${
        isVisible ? 'opacity-100' : 'opacity-0'
      } ${getTransform()} ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};

// --- Main Application ---
export default function App() {
  const [scrolled, setScrolled] = useState(false);

  // Handle sticky nav frosted glass effect
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#000000] text-zinc-50 font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      
      {/* Background Ambient Glow */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden flex justify-center">
        <div className="absolute top-[-20%] w-[800px] h-[600px] bg-indigo-600/20 blur-[120px] rounded-full mix-blend-screen opacity-50"></div>
        <div className="absolute top-[20%] right-[-10%] w-[600px] h-[600px] bg-purple-600/10 blur-[120px] rounded-full mix-blend-screen opacity-50"></div>
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${scrolled ? 'bg-black/50 backdrop-blur-xl border-b border-white/5 py-4' : 'bg-transparent py-6'}`}>
        <div className="max-w-7xl mx-auto px-6 md:px-12 flex justify-between items-center">
          <div className="text-xl font-semibold tracking-tighter">dev<span className="text-zinc-500">.pro</span></div>
          <div className="hidden md:flex space-x-8 text-sm font-medium text-zinc-400">
            <a href="#work" className="hover:text-white transition-colors">Work</a>
            <a href="#expertise" className="hover:text-white transition-colors">Expertise</a>
            <a href="#about" className="hover:text-white transition-colors">About</a>
          </div>
          <button className="bg-white text-black px-5 py-2 rounded-full text-sm font-semibold hover:scale-105 transition-transform duration-300 ease-out">
            Contact Me
          </button>
        </div>
      </nav>

      <main className="relative z-10 pt-32 md:pt-48 pb-24 px-6 md:px-12 max-w-7xl mx-auto">
        
        {/* Hero Section */}
        <section className="flex flex-col items-center text-center mb-40">
          <FadeIn>
            <div className="inline-flex items-center space-x-2 bg-zinc-900/50 border border-white/10 rounded-full px-4 py-1.5 mb-8 backdrop-blur-md">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-xs font-medium text-zinc-300 uppercase tracking-widest">Available for new projects</span>
            </div>
          </FadeIn>
          
          <FadeIn delay={100}>
            <h1 className="text-6xl md:text-8xl lg:text-[10rem] font-bold tracking-tighter leading-[0.9] mb-8">
              Engineer. <br className="hidden md:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-zinc-100 via-zinc-400 to-zinc-600">
                Designer.
              </span>
            </h1>
          </FadeIn>

          <FadeIn delay={200}>
            <p className="text-xl md:text-2xl text-zinc-400 max-w-2xl font-light tracking-tight mb-12">
              Crafting digital experiences where pixel-perfect design meets robust, scalable software architecture.
            </p>
          </FadeIn>

          <FadeIn delay={300} className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-6">
            <button className="flex items-center justify-center space-x-2 bg-white text-black px-8 py-4 rounded-full font-semibold text-lg hover:bg-zinc-200 hover:scale-105 transition-all duration-300">
              <span>View Portfolio</span>
              <ArrowRight size={20} />
            </button>
            <button className="flex items-center justify-center space-x-2 bg-zinc-900 border border-white/10 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-zinc-800 transition-all duration-300">
              <Github size={20} />
              <span>GitHub Profile</span>
            </button>
          </FadeIn>
        </section>

        {/* Bento Box Grid - Expertise */}
        <section id="expertise" className="mb-10 scroll-mt-32">
          <FadeIn>
            <h2 className="text-4xl md:text-5xl font-bold tracking-tighter mb-12">The capability to <br/>build anything.</h2>
          </FadeIn>
          
          <div className="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-6 h-auto md:h-[600px]">
            
            {/* Main Skill Card */}
            <FadeIn delay={0} className="md:col-span-2 md:row-span-2">
              <div className="h-full group relative overflow-hidden bg-zinc-900/40 border border-white/10 rounded-[2.5rem] p-10 hover:bg-zinc-800/50 transition-colors duration-500 flex flex-col justify-between">
                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 blur-[80px] rounded-full group-hover:bg-indigo-500/20 transition-all duration-700"></div>
                <div>
                  <Code2 className="text-indigo-400 mb-6" size={40} />
                  <h3 className="text-3xl font-semibold tracking-tight mb-4">Full-Stack Engineering</h3>
                  <p className="text-zinc-400 text-lg leading-relaxed max-w-md">
                    Building resilient, scalable systems from the database to the browser. Specializing in React, Node.js, and cloud infrastructure to deliver high-performance applications.
                  </p>
                </div>
                <div className="mt-12 flex flex-wrap gap-3">
                  {['React', 'TypeScript', 'Node.js', 'Next.js', 'PostgreSQL', 'AWS'].map(tech => (
                    <span key={tech} className="px-4 py-2 bg-black/50 border border-white/5 rounded-full text-sm font-medium text-zinc-300">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </FadeIn>

            {/* Sub Card 1 */}
            <FadeIn delay={100} className="md:col-span-1 md:row-span-1">
              <div className="h-full group relative overflow-hidden bg-zinc-900/40 border border-white/10 rounded-[2.5rem] p-8 hover:bg-zinc-800/50 transition-colors duration-500">
                <Layers className="text-purple-400 mb-6" size={32} />
                <h3 className="text-2xl font-semibold tracking-tight mb-3">UI/UX Design</h3>
                <p className="text-zinc-400">Pixel-perfect interfaces focusing on micro-interactions and accessibility.</p>
              </div>
            </FadeIn>

            {/* Sub Card 2 */}
            <FadeIn delay={200} className="md:col-span-1 md:row-span-1">
              <div className="h-full group relative overflow-hidden bg-zinc-900/40 border border-white/10 rounded-[2.5rem] p-8 hover:bg-zinc-800/50 transition-colors duration-500">
                <Zap className="text-emerald-400 mb-6" size={32} />
                <h3 className="text-2xl font-semibold tracking-tight mb-3">Performance</h3>
                <p className="text-zinc-400">Obsessed with sub-second load times, fluid 60fps animations, and optimization.</p>
              </div>
            </FadeIn>

          </div>
        </section>

      </main>
    </div>
  );
}