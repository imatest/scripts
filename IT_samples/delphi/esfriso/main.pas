{ February 2026 }
{==============================================================
*
* main.pas
* Delphi port of the C++ sample driver code that calls the Imatest
* IT shared library (imatest_library.dll) created using MATLAB Compiler.
*
* This executes the Imatest esfriso function on '.\esfriso_example.jpg'.
*
* Dependencies:
*   imatest_library.dll  - Imatest IT DLL
*   mclmcrrt.dll         - MATLAB Compiler Runtime (R2024b)
*
* The imatest_library.dll and MATLAB Runtime must be on the system PATH
* or in the same directory as this executable.
*
* Compiled with Delphi (any recent version supporting external DLLs).
*============================================================}

program main;

{$APPTYPE CONSOLE}

uses
  System.SysUtils,
  Winapi.Windows;

{ --------------------------------------------------------------------------
  mwArray is an opaque handle used by the MATLAB Compiler Runtime.
  The DLL exports C-callable wrappers that accept/return mwArray*.
  We represent it as a Pointer in Delphi.
  -------------------------------------------------------------------------- }
type
  TmwArray = Pointer;
  PmwArray = ^TmwArray;

  { Function type for mclRunMain callback }
  TmclMainFcnType = function(argc: Integer; argv: PPAnsiChar): Integer; cdecl;

{ --------------------------------------------------------------------------
  MATLAB Compiler Runtime (mclmcrrt) imports
  -------------------------------------------------------------------------- }
function  mclmcrInitialize: Boolean; cdecl; external 'mclmcrrt.dll';
function  mclInitializeApplication(const options: PPAnsiChar; count: Integer): Boolean; cdecl; external 'mclmcrrt.dll';
procedure mclTerminateApplication; cdecl; external 'mclmcrrt.dll';
function  mclRunMain(fn: TmclMainFcnType; argc: Integer; argv: PPAnsiChar): Integer; cdecl; external 'mclmcrrt.dll';

{ --------------------------------------------------------------------------
  imatest_library imports
  -------------------------------------------------------------------------- }
function  imatest_libraryInitialize: Boolean; cdecl; external 'imatest_library.dll';
procedure imatest_libraryTerminate; cdecl; external 'imatest_library.dll';
procedure it_terminate; cdecl; external 'imatest_library.dll';

{ mwArray construction / destruction }
function  mwCreateString(const s: PAnsiChar): TmwArray; cdecl; external 'imatest_library.dll';
procedure mwDestroyArray(arr: TmwArray); cdecl; external 'imatest_library.dll';

{ esfriso_shell:
    esfriso_shell(numOut, pOut, fileParam, pathParam, keysParam, modeParam, vararginParam)
  where numOut is the number of output arrays requested and pOut is a pointer
  to the first TmwArray output slot. }
procedure esfriso_shell(numOut: Integer; pOut: PmwArray;
                         fileParam, pathParam, keysParam,
                         modeParam, vararginParam: TmwArray); cdecl;
  external 'imatest_library.dll';

{ Helper to print an mwArray value as a string (the DLL exposes mwToString) }
function mwToString(arr: TmwArray): PAnsiChar; cdecl; external 'imatest_library.dll';

{ --------------------------------------------------------------------------
  run_main – equivalent to the C++ run_main function
  -------------------------------------------------------------------------- }
function run_main(argc: Integer; argv: PPAnsiChar): Integer; cdecl;
var
  args:        array[0..0] of PAnsiChar;
  argsPtr:     PPAnsiChar;
  count:       Integer;
  outArr:      TmwArray;
  fileParam:   TmwArray;
  pathParam:   TmwArray;
  keysParam:   TmwArray;
  modeParam:   TmwArray;
  vararginParam: TmwArray;
  resultStr:   PAnsiChar;
begin
  Result := 0;

  { Initialize the MATLAB Compiler Runtime application }
  args[0]  := '';
  argsPtr  := @args[0];
  count    := Length(args);

  if not mclInitializeApplication(argsPtr, count) then
  begin
    WriteLn('Error!');
    WriteLn(ErrOutput, 'could not initialize application properly');
    Result := -1;
    Exit;
  end;

  if not imatest_libraryInitialize then
  begin
    WriteLn('Error!');
    WriteLn(ErrOutput, 'could not initialize library properly');
    Result := -1;
    mclTerminateApplication;
    Exit;
  end;

  outArr        := nil;
  fileParam     := nil;
  pathParam     := nil;
  keysParam     := nil;
  modeParam     := nil;
  vararginParam := nil;

  try
    WriteLn('Watch me run!!');

    { Build input mwArray parameters.
      Adjust these paths to match your environment. }
    fileParam     := mwCreateString('.\esfriso_example.jpg');
    pathParam     := mwCreateString('..\Imatest_INI');
    keysParam     := mwCreateString('JSON');
    modeParam     := mwCreateString('-5');
    vararginParam := mwCreateString('');

    { Call the library function – request 1 output array }
    esfriso_shell(1, @outArr, fileParam, pathParam, keysParam, modeParam, vararginParam);

    { Print result }
    resultStr := mwToString(outArr);
    if resultStr <> nil then
      WriteLn('Your output: ', AnsiString(resultStr))
    else
      WriteLn('Your output: (nil)');

  except
    on E: Exception do
    begin
      WriteLn('Error!');
      WriteLn(ErrOutput, E.Message);
      Result := -2;
    end;
  end;

  { Clean up mwArray objects }
  if outArr        <> nil then mwDestroyArray(outArr);
  if fileParam     <> nil then mwDestroyArray(fileParam);
  if pathParam     <> nil then mwDestroyArray(pathParam);
  if keysParam     <> nil then mwDestroyArray(keysParam);
  if modeParam     <> nil then mwDestroyArray(modeParam);
  if vararginParam <> nil then mwDestroyArray(vararginParam);

  { Terminate library and application }
  it_terminate;
  imatest_libraryTerminate;
  mclTerminateApplication;
end;

{ --------------------------------------------------------------------------
  Program entry point
  -------------------------------------------------------------------------- }
begin
  try
    WriteLn('Watch me Start!!');
    mclmcrInitialize;
    WriteLn('Watch me Initialize!!');
    ExitCode := mclRunMain(@run_main, 0, nil);
  except
    on E: Exception do
    begin
      WriteLn(ErrOutput, 'Fatal: ', E.Message);
      ExitCode := -1;
    end;
  end;
end.
