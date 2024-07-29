import winston from 'winston'
//import ILogger from './Ilogger.ts

export interface ILogger {
  info(message: string): void
  debug(message: string): void
  error(message: string): void
  warn(message: string): void
}

export class Logger implements ILogger {
  private logger: winston.Logger

  constructor(file: string = 'pong.log') {
    const customFormat = winston.format.printf(({ timestamp, level, message }): string => {
      const levelStr = level.toUpperCase().padEnd(5)
      return `[${timestamp}] ${levelStr} ${message}`
    })

    this.logger = winston.createLogger({
      level: 'silly', // Incluye todos los niveles de log
      format: winston.format.combine(
        winston.format.timestamp(), // Formato de hora
        customFormat
      ),
      transports: [
        new winston.transports.Console(), // Transporte para la consola
        new winston.transports.File({ filename: file })
      ]
    })
  }

  info(mstr: string): void {
    this.logger.info(mstr)
  }

  debug(mstr: string): void {
    this.logger.debug(mstr)
  }

  error(mstr: string): void {
    this.logger.error(mstr)
  }

  warn(mstr: string): void {
    this.logger.warn(mstr)
  }
}
