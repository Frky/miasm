from miasm.core.types import MemStruct, Num, Ptr, Str, \
    Array, RawStruct, Union, \
    BitField, Self, Void, Bits, \
    set_allocator, MemUnion, Struct


class ListEntry64(MemStruct):
    fields = [
        ("flink", Ptr("<Q", Void())),
        ("blink", Ptr("<Q", Void())),
    ]


class PEB64_LDR_DATA(MemStruct):

    """
    +0x000 Length                          : Uint4B
    +0x004 Initialized                     : UChar
    +0x008 SsHandle                        : Ptr64 Void
    +0x010 InLoadOrderModuleList           : _LIST_ENTRY
    +0x020 InMemoryOrderModuleList         : _LIST_ENTRY
    +0x030 InInitializationOrderModuleList         : _LIST_ENTRY
    """

    fields = [
        ("Length", Num("<I")),
        ("Initialized", Num("<I")),
        ("SsHandle", Ptr("<Q", Void())),
        ("InLoadOrderModuleList", ListEntry64),
        ("InMemoryOrderModuleList", ListEntry64),
        ("InInitializationOrderModuleList", ListEntry64)
    ]


class PEB64(MemStruct):

    """
    +0x000 InheritedAddressSpace    : UChar
    +0x001 ReadImageFileExecOptions : UChar
    +0x002 BeingDebugged            : UChar
    +0x003 SpareBool                : UChar
    +0x004 Reserved                 : DWORD
    +0x008 Mutant                   : Ptr64 Void
    +0x010 ImageBaseAddress         : Ptr64 Void
    +0x018 Ldr                      : Ptr64 _PEB_LDR_DATA
    +0x020 processparameter
    """

    fields = [
        ("InheritedAddressSpace", Num("B")),
        ("ReadImageFileExecOptions", Num("B")),
        ("BeingDebugged", Num("B")),
        ("SpareBool", Num("B")),
        ("Reserved", Num("<I")),
        ("Mutant", Ptr("<Q", Void())),
        ("ImageBaseAddress", Num("<Q")),
        ("Ldr", Ptr("<Q", PEB64_LDR_DATA)),
    ]


class EXCEPTION64_REGISTRATION_RECORD(MemStruct):
    """
    +0x00 Next    : struct _EXCEPTION64_REGISTRATION_RECORD *
    +0x08 Handler : Ptr64 Void
    """

    fields = [
        ("Next", Ptr("<Q", Self())),
        ("Handler", Ptr("<Q", Void())),
    ]


class EXCEPTION64_RECORD(MemStruct):
    """
    DWORD                       ExceptionCode;
    DWORD                       ExceptionFlags;
    struct _EXCEPTION_RECORD_64 *ExceptionRecord;
    PVOID                       ExceptionAddress;
    DWORD                       NumberParameters;
    ULONG_PTR ExceptionInformation[EXCEPTION_MAXIMUM_PARAMETERS];
    """
    EXCEPTION_MAXIMUM_PARAMETERS = 15

    fields = [
        ("ExceptionCode", Num("<I")),
        ("ExceptionFlags", Num("<I")),
        ("ExceptionRecord", Ptr("<Q", Self())),
        ("ExceptionAddress", Ptr("<I", Void())),
        ("NumberParameters", Num("<I")),
        ("ExceptionInformation", Ptr("<I", Void())),
    ]


class NT_TIB64(MemStruct):

    """
    +00 struct _EXCEPTION_REGISTRATION_RECORD *ExceptionList
    +08 void *StackBase
    +10 void *StackLimit
    +18 void *SubSystemTib
    +20 void *FiberData
    +20 uint32 Version
    +28 void *ArbitraryUserPointer
    +30 struct _NT_TIB *Self
    """

    fields = [
        ("ExceptionList", Ptr("<Q", EXCEPTION64_REGISTRATION_RECORD)),
        ("StackBase", Ptr("<Q", Void())),
        ("StackLimit", Ptr("<Q", Void())),
        ("SubSystemTib", Ptr("<Q", Void())),
        (None, Union([
            ("FiberData", Ptr("<Q", Void())),
            ("Version", Num("<Q"))
        ])),
        ("ArbitraryUserPointer", Ptr("<Q", Void())),
        ("Self", Ptr("<Q", Self())),
    ]


class TEB64(MemStruct):

    """
    +0x000 NtTib                     : _NT_TIB64
    +0x038 EnvironmentPointer        : Ptr64 Void
    +0x040 ClientId                  : _CLIENT_ID
    +0x050 ActiveRpcHandle           : Ptr64 Void
    +0x058 ThreadLocalStoragePointer : Ptr64 Void
    +0x060 ProcessEnvironmentBlock   : Ptr64 _PEB
    +0x068 LastErrorValue            : Uint4B
    ...
    """

    fields = [
        ("NtTib", NT_TIB64),
        ("EnvironmentPointer", Ptr("<Q", Void())),
        ("ClientId", Array(Num("B"), 0x10)),
        ("ActiveRpcHandle", Ptr("<Q", Void())),
        ("ThreadLocalStoragePointer", Ptr("<Q", Void())),
        ("ProcessEnvironmentBlock", Ptr("<Q", PEB64)),
        ("LastErrorValue", Num("<Q")),
    ]
