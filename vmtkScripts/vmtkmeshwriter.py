#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkmeshwriter.py,v $
## Language:  Python
## Date:      $Date: 2006/07/27 08:27:40 $
## Version:   $Revision: 1.13 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.

import sys
import vtk
import vtkvmtk

import pypes

vmtkmeshwriter = 'vmtkMeshWriter'

class vmtkMeshWriter(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)

        self.Format = 'vtkxml'
        self.GuessFormat = 1
        self.OutputFileName = ''
        self.Mesh = None
        self.Input = None

        self.CellEntityIdsArrayName = ''

        self.SetScriptName('vmtkmeshwriter')
        self.SetScriptDoc('write a mesh to disk')
        self.SetInputMembers([
            ['Mesh','i','vtkUnstructuredGrid',1,'the input mesh','vmtkmeshreader'],
            ['Format','f','str',1,'file format (vtkxml, vtk, xda - libmesh ascii format, fdneut - FIDAP neutral format, pointdata)'],
            ['GuessFormat','guessformat','int',1,'guess file format from extension'],
            ['OutputFileName','ofile','str',1,'output file name'],
            ['OutputFileName','o','str',1,'output file name (deprecated: use -ofile)'],
            ['CellEntityIdsArrayName','entityidsarray','str',1,'name of the array where entity ids are stored']
            ])
        self.SetOutputMembers([])

    def WriteVTKMeshFile(self):
        if (self.OutputFileName == ''):
            self.PrintError('Error: no OutputFileName.')
        self.PrintLog('Writing VTK mesh file.')
        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetInput(self.Mesh)
        writer.SetFileName(self.OutputFileName)
        writer.Write()

    def WriteVTKXMLMeshFile(self):
        if (self.OutputFileName == ''):
            self.PrintError('Error: no OutputFileName.')
        self.PrintLog('Writing VTK XML mesh file.')
        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetInput(self.Mesh)
        writer.SetFileName(self.OutputFileName)
        writer.Write()

    def WriteXdaMeshFile(self):
        if (self.OutputFileName == ''):
            self.PrintError('Error: no OutputFileName.')
        self.PrintLog('Writing Xda mesh file.')
        writer = vtkvmtk.vtkvmtkXdaWriter()
        writer.SetInput(self.Mesh)
        writer.SetFileName(self.OutputFileName)
        if self.CellEntityIdsArrayName != '':
            writer.SetBoundaryDataArrayName(self.CellEntityIdsArrayName)
        writer.Write()

    def WriteFDNEUTMeshFile(self):
        if (self.OutputFileName == ''):
            self.PrintError('Error: no OutputFileName.')
        self.PrintLog('Writing FDNEUT mesh file.')
        writer = vtkvmtk.vtkvmtkFDNEUTWriter()
        writer.SetInput(self.Mesh)
        writer.SetFileName(self.OutputFileName)
        writer.Write()

    def WritePointDataMeshFile(self):
        if (self.OutputFileName == ''):
            self.PrintError('Error: no OutputFileName.')
        self.PrintLog('Writing PointData file.')
        f=open(self.OutputFileName, 'w')
        line = "X Y Z"
        arrayNames = []
        for i in range(self.Mesh.GetPointData().GetNumberOfArrays()):
            array = self.Mesh.GetPointData().GetArray(i)
            arrayName = array.GetName()
            if arrayName == None:
                continue
            if (arrayName[-1]=='_'):
                continue
            arrayNames.append(arrayName)
            if (array.GetNumberOfComponents() == 1):
                line = line + ' ' + arrayName
            else:
                for j in range(array.GetNumberOfComponents()):
                    line = line + ' ' + arrayName + str(j)
        line = line + '\n'
        f.write(line)
        for i in range(self.Mesh.GetNumberOfPoints()):
            point = self.Mesh.GetPoint(i)
            line = str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2])
            for arrayName in arrayNames:
                array = self.Mesh.GetPointData().GetArray(arrayName)
                for j in range(array.GetNumberOfComponents()):
                    line = line + ' ' + str(array.GetComponent(i,j))
            line = line + '\n'
            f.write(line)

    def Execute(self):

        if self.Mesh == None:
            if self.Input == None:
                self.PrintError('Error: no Mesh.')
            self.Mesh = self.Input

        extensionFormats = {'vtu':'vtkxml', 
                            'vtkxml':'vtkxml', 
                            'vtk':'vtk',
                            'xda':'xda',
                            'FDNEUT':'fdneut',
                            'dat':'pointdata'}

        if self.GuessFormat and self.OutputFileName:
            import os.path
            extension = os.path.splitext(self.OutputFileName)[1]
            if extension:
                extension = extension[1:]
                if extension in extensionFormats.keys():
                    self.Format = extensionFormats[extension]

        if (self.Format == 'vtk'):
            self.WriteVTKMeshFile()
        elif (self.Format == 'vtkxml'):
            self.WriteVTKXMLMeshFile()
        elif (self.Format == 'xda'):
            self.WriteXdaMeshFile()
        elif (self.Format == 'fdneut'):
            self.WriteFDNEUTMeshFile()
        elif (self.Format == 'pointdata'):
            self.WritePointDataMeshFile()
        else:
            self.PrintError('Error: unsupported format '+ self.Format + '.')


if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()