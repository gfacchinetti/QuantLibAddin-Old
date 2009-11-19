
/*  
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2005, 2006 Eric Ehlers
 
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
*/

// This file was generated automatically by gensrc.py.
// Editing this file manually is not recommended.

#include <oh/utilities.hpp>
#include <oh/ohdefines.hpp>
#include <qlo/qladdindefines.hpp>
#include <qlo/Enumerations/Factories/all.hpp>
#include <qlo/Conversions/all.hpp>
#include <oh/Enumerations/typefactory.hpp>
#include <qlo/options.hpp>
#include <qlo/payoffs.hpp>
#include <qlo/exercise.hpp>
#include <ql/instruments/oneassetoption.hpp>
#include <qlo/ValueObjects/vo_options.hpp>

#include <calcaddins.hpp>
#include <calcutils.hpp>
#include <conversions.hpp>

STRING SAL_CALL CalcAddins_impl::qlVanillaOption(
        const STRING &ObjectId,
        const STRING &Payoff,
        const STRING &Exercise,
        const ANY &Permanent,
        const ANY &Trigger,
        sal_Int32 Overwrite) throw (RuntimeException) {
    try {

        // convert input datatypes to C++ datatypes

        std::string ObjectIdCpp = ouStringToStlString(ObjectId);

        std::string PayoffCpp = ouStringToStlString(Payoff);

        std::string ExerciseCpp = ouStringToStlString(Exercise);

        bool PermanentCpp;
        calcToScalar(PermanentCpp, Permanent);

        // convert object IDs into library objects

        OH_GET_REFERENCE(PayoffLibObj, PayoffCpp,
            QuantLibAddin::StrikedTypePayoff, QuantLib::StrikedTypePayoff)

        OH_GET_REFERENCE(ExerciseLibObj, ExerciseCpp,
            QuantLibAddin::Exercise, QuantLib::Exercise)

        // Construct the Value Object

        boost::shared_ptr<ObjectHandler::ValueObject> valueObject(
            new QuantLibAddin::ValueObjects::qlVanillaOption(
                ObjectIdCpp,
                PayoffCpp,
                ExerciseCpp,
                PermanentCpp));

        // Construct the Object
        
        boost::shared_ptr<ObjectHandler::Object> object(
            new QuantLibAddin::VanillaOption(
                valueObject,
                PayoffLibObj,
                ExerciseLibObj,
                PermanentCpp));

        // Store the Object in the Repository

        std::string returnValue =
            ObjectHandler::Repository::instance().storeObject(ObjectIdCpp, object, Overwrite);

        // Convert and return the return value



        STRING returnValueCalc;
        scalarToCalc(returnValueCalc, returnValue);
        return returnValueCalc;

    } catch (const std::exception &e) {
        OH_LOG_MESSAGE("ERROR: qlVanillaOption: " << e.what());
        THROW_RTE;
    }
}


