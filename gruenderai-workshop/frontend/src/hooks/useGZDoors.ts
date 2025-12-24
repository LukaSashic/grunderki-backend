/**
 * GründerAI Workshop - useGZDoors Hook
 * Manages the state of the 7 GZ Doors (critical BA GZ 04 questions)
 */

import { useState, useCallback, useEffect } from 'react';
import type { GZDoor, GZDoorStatus, Module1Answers, CoachingExchange } from '@/types/module1.types';
import { INITIAL_GZ_DOORS } from '@/types/module1.types';
import { evaluateGZDoorStatus } from '@/services/coachingService';

interface UseGZDoorsReturn {
  doors: GZDoor[];
  updateDoorStatus: (doorId: string, status: GZDoorStatus) => void;
  evaluateAllDoors: (answers: Module1Answers, coachingHistory: CoachingExchange[]) => void;
  getDoorById: (doorId: string) => GZDoor | undefined;
  getPassedCount: () => number;
  getTotalCount: () => number;
  getDoorsForModule: (moduleId: number) => GZDoor[];
  resetDoors: () => void;
}

export const useGZDoors = (initialModule: number = 1): UseGZDoorsReturn => {
  const [doors, setDoors] = useState<GZDoor[]>(INITIAL_GZ_DOORS);

  // Update a single door's status
  const updateDoorStatus = useCallback((doorId: string, status: GZDoorStatus) => {
    setDoors(prev => prev.map(door =>
      door.id === doorId ? { ...door, status } : door
    ));
  }, []);

  // Evaluate all doors based on current answers and coaching history
  const evaluateAllDoors = useCallback((
    answers: Module1Answers,
    coachingHistory: CoachingExchange[]
  ) => {
    setDoors(prev => prev.map(door => {
      // Only evaluate doors for current module
      if (door.moduleId > initialModule) {
        return door;
      }

      const newStatus = evaluateGZDoorStatus(door.id, answers, coachingHistory);
      return { ...door, status: newStatus };
    }));
  }, [initialModule]);

  // Get a specific door by ID
  const getDoorById = useCallback((doorId: string) => {
    return doors.find(door => door.id === doorId);
  }, [doors]);

  // Get count of passed doors
  const getPassedCount = useCallback(() => {
    return doors.filter(door => door.status === 'passed').length;
  }, [doors]);

  // Get total door count
  const getTotalCount = useCallback(() => {
    return doors.length;
  }, [doors]);

  // Get doors relevant to a specific module
  const getDoorsForModule = useCallback((moduleId: number) => {
    return doors.filter(door => door.moduleId === moduleId);
  }, [doors]);

  // Reset all doors to initial state
  const resetDoors = useCallback(() => {
    setDoors(INITIAL_GZ_DOORS);
  }, []);

  return {
    doors,
    updateDoorStatus,
    evaluateAllDoors,
    getDoorById,
    getPassedCount,
    getTotalCount,
    getDoorsForModule,
    resetDoors
  };
};

// =============================================================================
// DOOR STATUS PERSISTENCE
// =============================================================================

const STORAGE_KEY = 'gruenderai-gz-doors';

export const useGZDoorsWithPersistence = (): UseGZDoorsReturn => {
  // Load initial state from localStorage
  const loadInitialState = (): GZDoor[] => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error('Failed to load GZ doors from storage:', e);
    }
    return INITIAL_GZ_DOORS;
  };

  const [doors, setDoors] = useState<GZDoor[]>(loadInitialState);

  // Persist to localStorage on change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(doors));
  }, [doors]);

  const updateDoorStatus = useCallback((doorId: string, status: GZDoorStatus) => {
    setDoors(prev => prev.map(door =>
      door.id === doorId ? { ...door, status } : door
    ));
  }, []);

  const evaluateAllDoors = useCallback((
    answers: Module1Answers,
    coachingHistory: CoachingExchange[]
  ) => {
    setDoors(prev => prev.map(door => {
      const newStatus = evaluateGZDoorStatus(door.id, answers, coachingHistory);
      return { ...door, status: newStatus };
    }));
  }, []);

  const getDoorById = useCallback((doorId: string) => {
    return doors.find(door => door.id === doorId);
  }, [doors]);

  const getPassedCount = useCallback(() => {
    return doors.filter(door => door.status === 'passed').length;
  }, [doors]);

  const getTotalCount = useCallback(() => {
    return doors.length;
  }, [doors]);

  const getDoorsForModule = useCallback((moduleId: number) => {
    return doors.filter(door => door.moduleId === moduleId);
  }, [doors]);

  const resetDoors = useCallback(() => {
    setDoors(INITIAL_GZ_DOORS);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return {
    doors,
    updateDoorStatus,
    evaluateAllDoors,
    getDoorById,
    getPassedCount,
    getTotalCount,
    getDoorsForModule,
    resetDoors
  };
};

export default useGZDoors;
