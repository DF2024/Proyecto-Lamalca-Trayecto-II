-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-07-2025 a las 10:00:19
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lamalca`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`) VALUES
(1, 'Electricidad'),
(2, 'Madera'),
(3, 'Cerraduras y corredores'),
(4, 'Herramientas'),
(5, 'Quimicos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cierres_caja`
--

CREATE TABLE `cierres_caja` (
  `id_cierre` int(11) NOT NULL,
  `fecha_apertura` datetime NOT NULL,
  `fecha_cierre` datetime DEFAULT NULL,
  `monto_inicial` decimal(10,2) NOT NULL,
  `ventas_sistema` decimal(10,2) DEFAULT NULL,
  `monto_final_contado` decimal(10,2) DEFAULT NULL,
  `diferencia` decimal(10,2) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cierres_caja`
--

INSERT INTO `cierres_caja` (`id_cierre`, `fecha_apertura`, `fecha_cierre`, `monto_inicial`, `ventas_sistema`, `monto_final_contado`, `diferencia`, `estado`, `observaciones`) VALUES
(11, '2025-07-08 03:19:52', '2025-07-08 03:26:12', 10.00, 124.30, 21111.00, 20976.70, 'CERRADA', ''),
(12, '2025-07-08 03:26:20', '2025-07-08 03:30:14', 20.00, 124.30, 5655.00, 5510.70, 'CERRADA', ''),
(13, '2025-07-08 03:35:41', '2025-07-08 03:35:52', 52.00, 124.30, 3333.00, 3156.70, 'CERRADA', ''),
(14, '2025-07-08 03:37:04', '2025-07-08 03:37:13', 20.00, 124.30, 5555.00, 5410.70, 'CERRADA', ''),
(15, '2025-07-08 03:43:16', '2025-07-08 03:47:25', 10.00, 124.30, 54555.00, NULL, '', ''),
(16, '2025-07-08 03:47:31', '2025-07-08 03:58:40', 10.00, 124.30, 222.00, NULL, '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `cedula` int(10) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `apellido`, `cedula`, `telefono`, `direccion`, `correo`) VALUES
(37, 'Andrés David', 'García Roa', 30443212, '04161772078', 'Barrio Obrero', 'ad79702@gmail.com'),
(38, 'David', 'Roa', 22675448, '04146165444', 'Barrio Obrero', 'correo@correo.com'),
(42, 'Juan', 'Diaz', 588566544, '6551681544', 'Los naranjos', 'correo@correo.com'),
(43, 'Deiviys', 'Uribe', 5622444, '145135544', 'La concordia', 'correo@correo.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id_compra` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_inventario` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`id_compra`, `id_cliente`, `id_inventario`, `cantidad`, `fecha`, `total`) VALUES
(13, NULL, 25, 10, '2025-07-02 00:00:00', 152.50),
(15, NULL, 25, 2, '2025-07-03 00:00:00', 30.50),
(17, NULL, 24, 10, '2025-07-03 00:00:00', 120.50),
(19, NULL, 24, 23, '2025-07-02 00:00:00', 277.15),
(21, NULL, 24, 12, '2025-07-03 00:00:00', 144.60),
(23, NULL, 24, 12, '2025-07-02 00:00:00', 144.60),
(25, NULL, 22, 10, '2025-07-03 00:00:00', 305.00),
(32, 37, 25, 10, '2025-07-03 00:00:00', 152.50),
(33, 37, 24, 6, '2025-07-09 00:00:00', 72.30),
(36, 37, 29, 2, '2025-07-02 00:00:00', 32.00),
(40, 37, 24, 1, '2025-07-02 00:00:00', 12.05),
(41, 37, 30, 5, '2025-07-11 00:00:00', 52.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` int(11) NOT NULL,
  `producto` varchar(50) DEFAULT NULL,
  `cantidad_actual` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `fecha_ultima_entrada` date DEFAULT NULL,
  `categoria` int(11) DEFAULT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `proveedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `producto`, `cantidad_actual`, `precio_unitario`, `fecha_ultima_entrada`, `categoria`, `observaciones`, `proveedor`) VALUES
(22, 'Bombillo', 110, 30.50, '2025-07-06', 1, 'Buenas condiciones', 4),
(24, 'Bombillo LED', 560, 12.05, '2025-07-06', 1, 'Buenas condiciones', 4),
(25, 'Toma Corriente', 128, 15.25, '2025-07-03', 1, 'Buenas condiciones', 4),
(29, 'Pino', 558, 50.66, '2025-07-02', 2, 'Vino en buenas condiciones', 16),
(30, 'Madera1', 145, 10.40, '2025-07-02', 2, 'Ta bien', 16);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `precio_venta` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `rif` varchar(50) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `rif`, `nombre`, `telefono`, `direccion`) VALUES
(4, '015000542', 'SuperElectricos', '04161772078', 'Pueblo Nuevo'),
(13, '15615655', 'Empresa', '65165444', 'Por ahi'),
(15, '15656455', 'Nuevo proveedor', '1565666', 'Barrio Obrero'),
(16, '45646111', 'Madera C.A', '04161772078', 'Barrio Obrero');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `cierres_caja`
--
ALTER TABLE `cierres_caja`
  ADD PRIMARY KEY (`id_cierre`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`cedula`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_inventario` (`id_inventario`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`),
  ADD UNIQUE KEY `uq_producto` (`producto`),
  ADD KEY `fk_producto_inventario` (`categoria`),
  ADD KEY `fk_proveedor_inventario` (`proveedor`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `cierres_caja`
--
ALTER TABLE `cierres_caja`
  MODIFY `id_cierre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_inventario`) REFERENCES `inventario` (`id_inventario`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `fk_proveedor_inventario` FOREIGN KEY (`proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
