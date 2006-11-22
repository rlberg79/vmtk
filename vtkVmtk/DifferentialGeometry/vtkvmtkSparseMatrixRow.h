/*=========================================================================

  Program:   VMTK
  Module:    $RCSfile: vtkvmtkSparseMatrixRow.h,v $
  Language:  C++
  Date:      $Date: 2006/04/06 16:46:44 $
  Version:   $Revision: 1.3 $

  Copyright (c) Luca Antiga, David Steinman. All rights reserved.
  See LICENCE file for details.

  Portions of this code are covered under the VTK copyright.
  See VTKCopyright.txt or http://www.kitware.com/VTKCopyright.htm 
  for details.

     This software is distributed WITHOUT ANY WARRANTY; without even 
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
// .NAME vtkvmtkSparseMatrixRow - ..
// .SECTION Description
// ..

#ifndef __vtkvmtkSparseMatrixRow_h
#define __vtkvmtkSparseMatrixRow_h

#include "vtkObject.h"
#include "vtkvmtkItem.h"
#include "vtkvmtkStencil.h"
#include "vtkvmtkConstants.h"
//#include "vtkvmtkDifferentialGeometryWin32Header.h"
#include "vtkvmtkWin32Header.h"

class VTK_VMTK_DIFFERENTIAL_GEOMETRY_EXPORT vtkvmtkSparseMatrixRow : public vtkvmtkItem 
{
public:

  static vtkvmtkSparseMatrixRow *New();
  vtkTypeRevisionMacro(vtkvmtkSparseMatrixRow,vtkvmtkItem);

  vtkIdType GetElementId(vtkIdType i) {return this->ElementIds[i];};
  void SetElementId(vtkIdType i, vtkIdType id) {this->ElementIds[i] = id;};

  double GetElement(vtkIdType i) {return this->Elements[i];};
  void SetElement(vtkIdType i, double element) {this->Elements[i] = element;};

  vtkIdType GetNumberOfElements() {return this->NElements;};
  void SetNumberOfElements(vtkIdType numberOfElements);

  vtkSetMacro(DiagonalElement,double);
  vtkGetMacro(DiagonalElement,double);

  virtual vtkIdType GetItemType() {return VTK_VMTK_SPARSE_MATRIX_ROW;};

  void Initialize();

  void CopyStencil(vtkvmtkStencil* stencil);

  // Description:
  // Standard DeepCopy method.  Since this object contains no reference
  // to other objects, there is no ShallowCopy.
  virtual void DeepCopy(vtkvmtkItem *src);

protected:
  vtkvmtkSparseMatrixRow();
  ~vtkvmtkSparseMatrixRow();

  vtkIdType* ElementIds;
  double* Elements;
  double DiagonalElement;
  vtkIdType NElements;

private:
  vtkvmtkSparseMatrixRow(const vtkvmtkSparseMatrixRow&);  // Not implemented.
  void operator=(const vtkvmtkSparseMatrixRow&);  // Not implemented.
};

#endif
