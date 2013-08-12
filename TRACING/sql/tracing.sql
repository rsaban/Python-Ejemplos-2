-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 10-08-2013 a las 18:46:18
-- Versión del servidor: 5.5.31
-- Versión de PHP: 5.3.10-1ubuntu3.7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `tracing`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `CENTRO`
--

CREATE TABLE IF NOT EXISTS `CENTRO` (
  `IdCentro` int(5) NOT NULL AUTO_INCREMENT,
  `NombreCentro` varchar(300) COLLATE utf8_spanish_ci DEFAULT NULL,
  `TipoCentro` varchar(30) COLLATE utf8_spanish_ci DEFAULT NULL,
  `Tipologia` varchar(50) COLLATE utf8_spanish_ci DEFAULT NULL,
  `Grupo` int(5) DEFAULT NULL,
  PRIMARY KEY (`IdCentro`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `DEPENDIENTE`
--

CREATE TABLE IF NOT EXISTS `DEPENDIENTE` (
  `Expdte` varchar(30) COLLATE utf8_spanish_ci NOT NULL,
  `Nombre` varchar(200) COLLATE utf8_spanish_ci DEFAULT NULL,
  `IdCentro` int(5) DEFAULT NULL,
  `Estado` varchar(20) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`Expdte`),
  KEY `IdCentro` (`IdCentro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `INFORMES`
--

CREATE TABLE IF NOT EXISTS `INFORMES` (
  `IdInforme` int(20) NOT NULL AUTO_INCREMENT,
  `FechaInforme` date DEFAULT NULL,
  `Observaciones` mediumtext COLLATE utf8_spanish_ci,
  `PDF` longblob,
  `IdCentro` int(5) DEFAULT NULL,
  `Expdte` varchar(30) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`IdInforme`),
  KEY `IdCentro` (`IdCentro`,`Expdte`),
  KEY `Expdte` (`Expdte`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=16 ;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `DEPENDIENTE`
--
ALTER TABLE `DEPENDIENTE`
  ADD CONSTRAINT `DEPENDIENTE_ibfk_1` FOREIGN KEY (`IdCentro`) REFERENCES `CENTRO` (`IdCentro`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `INFORMES`
--
ALTER TABLE `INFORMES`
  ADD CONSTRAINT `INFORMES_ibfk_1` FOREIGN KEY (`IdCentro`) REFERENCES `CENTRO` (`IdCentro`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `INFORMES_ibfk_2` FOREIGN KEY (`Expdte`) REFERENCES `DEPENDIENTE` (`Expdte`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
