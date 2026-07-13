@echo off
setlocal enabledelayedexpansion

REM =====================================================
REM Remove ALL MinGW/MSYS paths
REM =====================================================
for %%i in (
  C:\mingw64\bin
  C:\msys64\mingw64\bin
  C:\msys64\usr\bin
  C:\msys64\bin
) do (
  set "PATH=!PATH:%%i;=!"
)

echo =====================================================
echo BEFORE MSVC activation:
echo =====================================================

where cl
where gcc
where g++
echo PATH:
echo %PATH%

REM =====================================================
REM Install Ninja
REM =====================================================
choco install ninja

REM =====================================================
REM Activate MSVC environment
REM =====================================================
call "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"

echo =====================================================
echo AFTER MSVC activation:
echo =====================================================

where cl
where gcc
where g++
echo PATH:
echo %PATH%

REM =====================================================
REM Configure CMake
REM =====================================================
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DPLUGIN_FORMATS=VST3

REM =====================================================
REM Build
REM =====================================================
cmake --build build --config Release
