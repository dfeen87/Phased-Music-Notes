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

echo BEFORE MSVC activation:
where cl
where gcc
where g++
echo PATH:
echo %PATH%

REM Install Ninja
choco install ninja

REM Activate MSVC environment
call "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"

echo AFTER MSVC activation:
where cl
where gcc
where g++
echo PATH:
echo %PATH%

REM Configure CMake
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DPLUGIN_FORMATS=VST3

REM Build
cmake --build build --config Release
