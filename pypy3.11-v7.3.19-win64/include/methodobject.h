
/* Method object interface */

#ifndef Py_METHODOBJECT_H
#define Py_METHODOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif
// Cast an function to the PyCFunction type to use it with PyMethodDef.
//
// This macro can be used to prevent compiler warnings if the first parameter
// uses a different pointer type than PyObject* (ex: METH_VARARGS and METH_O
// calling conventions).
//
// The macro can also be used for METH_FASTCALL and METH_VARARGS|METH_KEYWORDS
// calling conventions to avoid compiler warnings because the function has more
// than 2 parameters. The macro first casts the function to the
// "void func(void)" type to prevent compiler warnings.
//
// If a function is declared with the METH_NOARGS calling convention, it must
// have 2 parameters. Since the second parameter is unused, Py_UNUSED() can be
// used to prevent a compiler warning. If the function has a single parameter,
// it triggers an undefined behavior when Python calls it with 2 parameters
// (bpo-33012).
#define _PyCFunction_CAST(func) \
    _Py_CAST(PyCFunction, _Py_CAST(void(*)(void), (func)))


/* Flag passed to newmethodobject */
#define METH_VARARGS  0x0001
#define METH_KEYWORDS 0x0002
/* METH_NOARGS and METH_O must not be combined with the flags above. */
#define METH_NOARGS   0x0004
#define METH_O        0x0008

/* METH_CLASS and METH_STATIC are a little different; these control
   the construction of methods for a class.  These cannot be used for
   functions in modules. */
#define METH_CLASS    0x0010
#define METH_STATIC   0x0020

/* METH_COEXIST allows a method to be entered eventhough a slot has
   already filled the entry.  When defined, the flag allows a separate
   method, "__contains__" for example, to coexist with a defined 
   slot like sq_contains. */

#define METH_COEXIST   0x0040

#if !defined(Py_LIMITED_API) || Py_LIMITED_API+0 >= 0x030A0000
#define METH_FASTCALL  0x0080
#endif

/* METH_METHOD means the function stores an
 * additional reference to the class that defines it;
 * both self and class are passed to it.
 * It uses PyCMethodObject instead of PyCFunctionObject.
 * May not be combined with METH_NOARGS, METH_O, METH_CLASS or METH_STATIC.
 */

#if !defined(Py_LIMITED_API) || Py_LIMITED_API+0 >= 0x03090000
#define METH_METHOD 0x0200
#endif


#define PyCFunction_New(ml, self) PyCFunction_NewEx((ml), (self), NULL)
#define PyCFunction_NewEx(ML, SELF, MOD) PyCMethod_New((ML), (SELF), (MOD), NULL)


/* Macros for direct access to these values. Type checks are *not*
   done, so use with care. */
#define PyCFunction_GET_FUNCTION(func) \
        (((PyCFunctionObject *)func) -> m_ml -> ml_meth)
#define PyCFunction_GET_SELF(func) \
        (((PyCFunctionObject *)func) -> m_ml -> ml_flags & METH_STATIC ? \
         NULL : ((PyCFunctionObject *)func) -> m_self)
#define PyCFunction_GET_FLAGS(func) \
        (((PyCFunctionObject *)func) -> m_ml -> ml_flags)
#define PyCFunction_GET_CLASS(func) \
    (((PyCFunctionObject *)func) -> m_ml -> ml_flags & METH_METHOD ? \
         ((PyCMethodObject *)func) -> mm_class : NULL)

#ifdef __cplusplus
}
#endif
#endif /* !Py_METHODOBJECT_H */
