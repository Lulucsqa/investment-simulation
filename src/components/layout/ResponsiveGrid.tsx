import React from 'react';
import { cn } from '@/lib/utils';

interface ResponsiveGridProps {
  children: React.ReactNode;
  className?: string;
  columns?: {
    xs?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    '2xl'?: number;
  };
  gap?: 'sm' | 'md' | 'lg' | 'xl';
}

const getGridCols = (cols: number) => {
  const colsMap = {
    1: 'grid-cols-1',
    2: 'grid-cols-2',
    3: 'grid-cols-3',
    4: 'grid-cols-4',
    5: 'grid-cols-5',
    6: 'grid-cols-6',
    12: 'grid-cols-12',
  };
  return colsMap[cols as keyof typeof colsMap] || 'grid-cols-1';
};

const gapClasses = {
  sm: 'gap-2 sm:gap-3',
  md: 'gap-3 sm:gap-4 lg:gap-6',
  lg: 'gap-4 sm:gap-6 lg:gap-8',
  xl: 'gap-6 sm:gap-8 lg:gap-12',
};

export const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({
  children,
  className,
  columns = { xs: 1, sm: 2, lg: 3 },
  gap = 'md',
}) => {
  const gridClasses = [
    'grid',
    columns.xs && getGridCols(columns.xs),
    columns.sm && `sm:${getGridCols(columns.sm)}`,
    columns.md && `md:${getGridCols(columns.md)}`,
    columns.lg && `lg:${getGridCols(columns.lg)}`,
    columns.xl && `xl:${getGridCols(columns.xl)}`,
    columns['2xl'] && `2xl:${getGridCols(columns['2xl'])}`,
    gapClasses[gap],
  ].filter(Boolean);

  return (
    <div className={cn(gridClasses.join(' '), className)}>
      {children}
    </div>
  );
};

export default ResponsiveGrid;