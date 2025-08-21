import { supabase } from '@/integrations/supabase/client';
import { withErrorHandling, withRetry, handleSupabaseError } from '@/lib/error-handling';
import { logger } from '@/lib/logger';
import type { SimulationResult } from '@/types/investment';

export const investmentService = {
  saveSimulation: async (simulation: SimulationResult) => {
    return withErrorHandling(async () => {
      const { data, error } = await withRetry(() => 
        supabase
          .from('simulations')
          .insert([simulation])
          .select()
          .single()
      );

      if (error) {
        handleSupabaseError(error);
        throw error;
      }

      logger.info('Simulation saved successfully', { id: data.id });
      return data;
    }, 'saveSimulation');
  },

  getSimulations: async (userId: string) => {
    return withErrorHandling(async () => {
      const { data, error } = await supabase
        .from('simulations')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });

      if (error) {
        handleSupabaseError(error);
        throw error;
      }

      return data;
    }, 'getSimulations');
  },

  getSimulationById: async (id: string) => {
    return withErrorHandling(async () => {
      const { data, error } = await supabase
        .from('simulations')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        handleSupabaseError(error);
        throw error;
      }

      return data;
    }, 'getSimulationById');
  },

  deleteSimulation: async (id: string) => {
    return withErrorHandling(async () => {
      const { error } = await supabase
        .from('simulations')
        .delete()
        .eq('id', id);

      if (error) {
        handleSupabaseError(error);
        throw error;
      }

      logger.info('Simulation deleted successfully', { id });
    }, 'deleteSimulation');
  }
};
