import { useState, useEffect } from 'react';

interface ResponsiveConfig {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
  '2xl': number;
}

const breakpoints: ResponsiveConfig = {
  xs: 475,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
};

export type BreakpointKey = keyof ResponsiveConfig;

export const useResponsive = () => {
  const [currentBreakpoint, setCurrentBreakpoint] = useState<BreakpointKey>('xs');
  const [screenWidth, setScreenWidth] = useState<number>(0);

  useEffect(() => {
    const updateBreakpoint = () => {
      const width = window.innerWidth;
      setScreenWidth(width);

      if (width >= breakpoints['2xl']) {
        setCurrentBreakpoint('2xl');
      } else if (width >= breakpoints.xl) {
        setCurrentBreakpoint('xl');
      } else if (width >= breakpoints.lg) {
        setCurrentBreakpoint('lg');
      } else if (width >= breakpoints.md) {
        setCurrentBreakpoint('md');
      } else if (width >= breakpoints.sm) {
        setCurrentBreakpoint('sm');
      } else {
        setCurrentBreakpoint('xs');
      }
    };

    // Set initial values
    updateBreakpoint();

    // Add event listener
    window.addEventListener('resize', updateBreakpoint);

    // Cleanup
    return () => window.removeEventListener('resize', updateBreakpoint);
  }, []);

  const isBreakpoint = (breakpoint: BreakpointKey) => {
    return screenWidth >= breakpoints[breakpoint];
  };

  const isMobile = !isBreakpoint('md');
  const isTablet = isBreakpoint('md') && !isBreakpoint('lg');
  const isDesktop = isBreakpoint('lg');

  return {
    currentBreakpoint,
    screenWidth,
    isBreakpoint,
    isMobile,
    isTablet,
    isDesktop,
    breakpoints,
  };
};

export default useResponsive;