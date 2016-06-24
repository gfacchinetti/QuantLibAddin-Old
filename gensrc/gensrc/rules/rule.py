
"""
 Copyright (C) 2005, 2006, 2007, 2008 Eric Ehlers
 Copyright (C) 2005 Plamen Neykov
 Copyright (C) 2005 Aurelien Chanudet

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <http://quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

"""Algorithms required to generate the source code for a given function 
parameter in a given context."""

from gensrc.rules import exceptions
from gensrc.configuration import environment
from gensrc.serialization import serializable
from gensrc.utilities import common
import sys
import os
# The following allows the client application to place file codedict.py
# in subdirectory 'code' of current directory.
sys.path.append(os.getcwd() + '/code')
import codedict

def getCode(codeID):
    """Retrieve the requested item from module codedict.py"""
    if codedict.__dict__.has_key(codeID):
        return codedict.__dict__[codeID]
    else:
        raise exceptions.RuleCodeInvalidException(codeID)

class Rule(serializable.Serializable):
    """The subset of a Rule pertaining to one or more tensor ranks."""

    #############################################
    # class variables
    #############################################

    groupName_ = 'Rules'
    
    tensorRank_ = None
    superType_ = None
    nativeType_ = None    
    type_ = None
    nameSpace_= None
    default_ = None
    error_ = None
    loop_ = None
    codeID_ = None
    vectorIterator_ = None
    const_ = None
    objectReference_ = None

    #############################################
    # public interface           
    #############################################

    def match(self, param):
        return (self.tensorRank_ == None or self.tensorRank_ == param.tensorRank()) \
            and (self.superType_ == None or self.superType_ == param.fullType().superType()) \
            and (self.nativeType_ == None or self.nativeType_ == param.fullType().nativeType()) \
            and (self.type_ == None or self.type_ == param.fullType().value()) \
            and (self.objectReference_ == None or self.objectReference_ == param.fullType().objectReference()) \
            and (self.vectorIterator_ == None or self.vectorIterator_ == param.vectorIterator()) \
            and (self.default_ == None or self.default_ == bool(param.default())) \
            and (self.error_ == None or self.error_ == bool(param.errorValue())) \
            and (self.loop_ == None or self.loop_ == bool(param.loop())) \
            and (self.const_ == None or self.const_ == bool(param.const()))

    def code(self):
        return self.code_

    def printDebug(self):
        print self.tensorRank_, self.superType_, self.nativeType_, self.type_, \
            self.default_, self.loop_, self.code_

    #############################################
    # serializer interface
    #############################################

    def serialize(self, serializer):
        """Load/unload class state to/from serializer object."""
        serializer.serializeAttribute(self, common.TENSOR_RANK)
        serializer.serializeAttribute(self, common.SUPER_TYPE)
        serializer.serializeAttribute(self, common.NATIVE_TYPE)
        serializer.serializeAttribute(self, common.TYPE)
        serializer.serializeAttribute(self, common.VECTOR_ITERATOR)
        serializer.serializeAttributeBoolean(self, common.DEFAULT)
        serializer.serializeAttributeBoolean(self, common.ERROR)
        serializer.serializeAttributeBoolean(self, common.LOOP)
        serializer.serializeAttributeBoolean(self, common.CONST)
        serializer.serializeAttributeBoolean(self, common.OBJECT_REFERENCE)
        serializer.serializeAttribute(self, common.CODE_ID)
        serializer.serializeValue(self)

    def postSerialize(self):
        """Perform post serialization initialization."""
        if self.codeID_:
            self.code_ = getCode(self.codeID_)
        else:
            self.code_ = self.value_

class Wrap(serializable.Serializable):
    """A class to process the 'wrap' text for a rule.  If this class
    is specified in the XML, then ParameterList will invoke it after the
    Rule is processed e.g.
        T = W % R
    where R is the text derived from Rule, W is the value of Wrap, and
    T is the final text to be returned to the Addin.

    This can be used e.g. when the autogenerated code needs to be prefixed
    and/or suffixed with comments."""

    #############################################
    # class variables
    #############################################

    name_ = 'Wrap'

    #############################################
    # public interface
    #############################################

    def text(self):
        return self.text_

    #############################################
    # serializer interface
    #############################################

    def serialize(self, serializer):
        """Load/unload class state to/from serializer object."""
        serializer.serializeValue(self)
        serializer.serializeAttribute(self, common.CODE_ID)

    def postSerialize(self):
        if self.codeID_:
            self.text_ = getCode(self.codeID_)
        else:
            self.text_ = self.value_

class RuleGroup(serializable.Serializable):
    """This class encapsulates an algorithm required to generate the source
    code for a given function parameter in a given context."""

    #############################################
    # class variables
    #############################################

    groupName_ = 'RuleGroups'

    #############################################
    # public interface
    #############################################

    def apply(self, param):
        """Apply all available Rules to given parameter."""

        if self.checkParameterIgnore_ and param.ignore(): return

        if self.padLastParamDesc_ and param.lastParameter():
            self.paramDesc_ = param.description() + '  '
        else:
            self.paramDesc_ = param.description()

        self.param_ = param

        if self.applyRule():
            return self.invokeRule()

    def applyRule(self):
        """Apply the Rule, if any, which matches the given parameter"""
        for ruleItem in self.rules_:
            if ruleItem.match(self.param_):
                self.ruleResult_ = ruleItem.code()
                return self.ruleResult_ != None

    def invokeRule(self):

        return self.ruleResult_ % {
            'classname' : self.param_.fullType().classname(),
            common.DEFAULT_VALUE : self.param_.default(),
            common.DESC_LEN : len(self.paramDesc_),
            common.DESCRIPTION : self.paramDesc_,
            common.ERROR_VALUE : self.param_.errorValue(),
            common.INDENT2 : self.indent_ + '    ',
            common.INDENT : self.indent_,
            common.NAME : self.param_.name(),
            common.NAME_CONVERTED : self.param_.nameConverted(),
            common.NAME_UPPER : self.param_.name().upper(),
            common.NAMESPACE_LIB : environment.config().namespaceLibrary(),
            common.NAMESPACE_OBJ : environment.config().namespaceObjects(),
            common.NATIVE_TYPE : self.param_.fullType().nativeType(),
            common.OBJECT_REFERENCE : self.param_.fullType().objectReference(),
            common.SUPER_TYPE : self.param_.fullType().superType(),
            common.TENSOR_RANK : self.param_.tensorRank(),
            common.TYPE : self.param_.fullType().value() ,
            common.NAMESPACE : self.param_.nameSpace() }

    def checkSkipFirst(self):
        return self.checkSkipFirst_

    def delimiter(self):
        return self.delimiter_

    def wrapText(self):
        return self.wrapText_

    def printDebug(self):
        """Write debug information to stdout."""
        print "debug rule group *****"
        print self.name_, self.delimiter_, self.checkParameterIgnore_, \
            self.checkSkipFirst_, self.indent_
        for ruleItem in self.rules_:
            print "print rule item: *****"
            ruleItem.printDebug()

    #############################################
    # serializer interface
    #############################################

    def serialize(self, serializer):
        """Load/unload class state to/from serializer object."""
        serializer.serializeAttribute(self, common.NAME)
        serializer.serializeAttribute(self, common.DELIM, '')
        serializer.serializeAttributeBoolean(self, common.CHECK_PARAM_IGNORE)
        serializer.serializeAttributeBoolean(self, common.CHECK_SKIP_FIRST)
        serializer.serializeAttributeBoolean(self, common.PAD_LAST_PARAM)
        serializer.serializeAttributeBoolean(self, common.OBJECT_REFERENCE)
        serializer.serializeAttributeInteger(self, common.INDENT, 0)
        serializer.serializeObject(self, Wrap)
        serializer.serializeObjectList(self, Rule)

    def postSerialize(self):
        """Perform post serialization initialization."""
        self.indent_ *= 4 * ' '
        if self.wrap_:
            self.wrapText_ = self.wrap_.text()
        else:
            self.wrapText_ = None

