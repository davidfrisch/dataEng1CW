import express from 'express'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
const app = express()

export default {
  
  getRuns: async () => {
    const results = prisma.protein_results.findMany({
      distinct: ['run_id'],
      select: {
        run_id: true
      }
    })
    
    return results
  },
  
  getProteins: async (run_id) => {
    const results = prisma.protein_results.findMany({
      where: {
        run_id: run_id
      }
    })
    
    return results
  },

  toCSV: (proteins) => {
    const header = Object.keys(proteins[0]).join(',')
    const rows = proteins.map(row => Object.values(row).join(','))
    return [header, ...rows].join('\n')
  }
 
}